import logging
import tempfile
import pandas as pd

from tqdm import tqdm
from qa4iqi_extraction.constants import (
    SERIES_DESCRIPTION_FIELD,
    SERIES_NUMBER_FIELD,
    STUDY_UID_FIELD,
)
from qa4iqi_extraction.features.extract_features import extract_features

from qa4iqi_extraction.utils.nifti import convert_to_nifti

logger = logging.getLogger()


def run_feature_extraction(dicom_folders_map):
    logger.info("Running feature extraction...")

    i = 0
    all_features_df = []
    for study_uid, dicom_image_mask in tqdm(
        dicom_folders_map.items(), desc="Processing all DICOM studies"
    ):
        with tempfile.TemporaryDirectory(prefix=study_uid) as tmp_dir:
            nifti_image_path, nifti_roi_paths, dicom_info = convert_to_nifti(
                dicom_image_mask, tmp_dir
            )
            logger.debug(f"Done converting study {study_uid}")

            features_df = extract_features(
                nifti_image_path, nifti_roi_paths, dicom_info[SERIES_DESCRIPTION_FIELD]
            )

            features_df.insert(
                0, SERIES_DESCRIPTION_FIELD, dicom_info[SERIES_DESCRIPTION_FIELD]
            )
            features_df.insert(0, SERIES_NUMBER_FIELD, dicom_info[SERIES_NUMBER_FIELD])
            features_df.insert(0, STUDY_UID_FIELD, study_uid)

            all_features_df.append(features_df)

        i += 1

    # Concatenate all dataframes
    concatenated_features_df = pd.concat(all_features_df, ignore_index=True)

    # Sort by series number
    concatenated_features_df = concatenated_features_df.sort_values(SERIES_NUMBER_FIELD)

    return concatenated_features_df
