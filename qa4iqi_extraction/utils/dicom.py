import os
import logging
import json

from glob import glob
from pydicom import dcmread
from tqdm import tqdm

from qa4iqi_extraction.constants import (
    FIELD_NAME_IMAGE,
    FIELD_NAME_SEG,
    MODALITY_CT,
    MODALITY_SEG,
)

logger = logging.getLogger()


def identify_images_rois(folder):
    logger.info("Identifying Image & ROI pairs...")

    # Check if map is already available
    map_file_path = f"{folder}/studies_map.json"

    if os.path.exists(map_file_path):
        logger.info("Existing mapping found!")
        with open(map_file_path, "r") as map_file:
            study_folders_map = json.load(map_file)
            return study_folders_map

    series_folders = [f for f in os.listdir(folder) if os.path.isdir(folder)]

    study_folders_map = {}

    # Read one file from each folder to identify Image -> ROI pairs
    for series_folder in tqdm(series_folders):
        dicom_files = glob(f"{folder}/{series_folder}/*.dcm")
        first_dicom_file = dicom_files[0]
        ds = dcmread(first_dicom_file, defer_size="1 KB", stop_before_pixels=True)

        # Check if it's the image or the ROIs
        study_uid = ds.StudyInstanceUID
        modality = ds.Modality

        if study_uid not in study_folders_map:
            study_folders_map[study_uid] = {}

        if modality == MODALITY_CT:
            study_folders_map[study_uid][FIELD_NAME_IMAGE] = os.path.dirname(
                first_dicom_file
            )
        elif modality == MODALITY_SEG:
            study_folders_map[study_uid][FIELD_NAME_SEG] = first_dicom_file
        else:
            raise ValueError(f"Modality {modality} is not supported")

    with open(map_file_path, "w") as map_file:
        json.dump(study_folders_map, map_file)

    return study_folders_map
