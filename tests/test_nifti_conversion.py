import os
import tempfile
from qa4iqi_extraction.utils.nifti import convert_to_nifti


def test_nifti_conversion():
    dicom_folder = os.getenv(
        "DICOM_DIR_PATH"
    )  # Indicate path to a DICOM series folder from the dataset
    dicom_seg_file = os.getenv(
        "DICOMSEG_FILE_PATH"
    )  # Indicate path to corresponding DICOM-SEG file

    assert dicom_folder is not None and os.path.isdir(
        dicom_folder
    ), "Path to DICOM folder needs to be specified in DICOM_DIR variable in .env at the root of your workspace"
    assert dicom_seg_file is not None and os.path.isfile(
        dicom_seg_file
    ), "Path to DICOM SEG file needs to be specified in DICOM_DIR variable in .env at the root of your workspace"

    with tempfile.TemporaryDirectory(prefix="qa4iqi_extraction") as tmp_dir:
        input_map = {"image": dicom_folder, "seg": dicom_seg_file}
        nifti_image_path, nifti_roi_paths, dicom_info = convert_to_nifti(
            input_map, tmp_dir
        )

        # Check that all files were correctly generated
        assert os.path.isfile(nifti_image_path)

        for nifti_roi_path in nifti_roi_paths:
            assert os.path.isfile(nifti_roi_path)
