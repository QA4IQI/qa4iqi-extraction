from glob import glob
import os
import numpy as np
import nibabel as nib
import dcmstack
import pydicom
import pydicom_seg


from qa4iqi_extraction.constants import (
    FIELD_NAME_IMAGE,
    FIELD_NAME_SEG,
    FOLDER_NAME_IMAGE,
    FOLDER_NAME_ROIS,
    SERIES_DESCRIPTION_FIELD,
    SERIES_NUMBER_FIELD,
)


def convert_to_nifti(dicom_image_mask, nifti_dir):
    output_folder_image = f"{nifti_dir}/{FOLDER_NAME_IMAGE}"
    output_folder_rois = f"{nifti_dir}/{FOLDER_NAME_ROIS}"
    output_file_seg_prefix = "segmentation"
    output_file_seg_suffix = ".nii.gz"

    os.makedirs(output_folder_image, exist_ok=True)
    os.makedirs(output_folder_rois, exist_ok=True)

    dicom_image_folder = dicom_image_mask[FIELD_NAME_IMAGE]
    dicom_seg_file = dicom_image_mask[FIELD_NAME_SEG]

    # Read DICOM image & convert to NIfTI
    dicom_files = glob(f"{dicom_image_folder}/*.dcm")
    dicom_datasets = [pydicom.dcmread(f) for f in dicom_files]
    dicom_datasets = sorted(dicom_datasets, key=lambda ds: -ds.InstanceNumber)

    # Store useful DICOM metadata
    dicom_info = {}
    dicom_info[SERIES_NUMBER_FIELD] = dicom_datasets[0].SeriesNumber
    dicom_info[SERIES_DESCRIPTION_FIELD] = dicom_datasets[0].SeriesDescription

    stack = dcmstack.DicomStack()
    for ds in dicom_datasets:
        stack.add_dcm(ds)
    nii = stack.to_nifti()
    nifti_image_path = f"{output_folder_image}/image.nii.gz"
    nii.to_filename(nifti_image_path, dtype=np.uint16)

    # Read DICOM SEG & convert to NIfTI
    dicom_seg = pydicom.dcmread(dicom_seg_file)
    reader = pydicom_seg.SegmentReader()
    result = reader.read(dicom_seg)

    # Get index to label mapping
    segment_labels = [s.SegmentLabel for s in dicom_seg.SegmentSequence]

    # Find smallest patient Z position to define starting index
    all_instance_z_locations = [
        float(ds.ImagePositionPatient[-1]) for ds in dicom_datasets
    ]

    all_referenced_z_locations = [
        float(f.PlanePositionSequence[0].ImagePositionPatient[-1])
        for f in dicom_seg.PerFrameFunctionalGroupsSequence
    ]
    all_referenced_z_locations = np.unique(all_referenced_z_locations)

    min_referenced_z_location = min(all_referenced_z_locations)

    starting_index_global = all_instance_z_locations.index(min_referenced_z_location)
    ending_index_global = starting_index_global + len(all_referenced_z_locations)

    # Write out each ROI to a separate file (simpler for pyradiomics extraction)
    nifti_roi_paths = []
    for segment_number in result.available_segments:
        segmentation_image_data = result.segment_data(segment_number)

        # change axes to match dicom
        seg = np.fliplr(np.swapaxes(segmentation_image_data, 0, -1))

        # pad segmentation to match dicom dimensions
        padded_seg = pad_segmentation(
            seg, stack.shape, starting_index_global, ending_index_global
        )

        padded_seg_image = nib.nifti1.Nifti1Image(padded_seg, nii.affine, nii.header)

        nifti_roi_path = f"{output_folder_rois}/{output_file_seg_prefix}-{segment_number}-{segment_labels[segment_number - 1]}{output_file_seg_suffix}"
        nifti_roi_paths.append(nifti_roi_path)

        padded_seg_image.to_filename(nifti_roi_path, dtype=np.uint8)

    return nifti_image_path, nifti_roi_paths, dicom_info


def pad_segmentation(segmentation, reference_image_shape, starting_index, ending_index):
    padded_seg = np.zeros(reference_image_shape, dtype=np.uint8)

    padded_seg[:, :, starting_index:ending_index] = segmentation

    return padded_seg
