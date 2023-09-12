import os
import logging

from dotenv import load_dotenv

from qa4iqi_extraction.constants import DATASET_FOLDER, OUTPUT_FILE_NAME
from qa4iqi_extraction.data.check_data import check_data
from qa4iqi_extraction.data.download_data import offer_download_data
from qa4iqi_extraction.utils.dicom import identify_images_rois
from qa4iqi_extraction.features.feature_extraction import run_feature_extraction

load_dotenv()

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())

if __name__ == "__main__":
    # Paths
    dataset_folder = DATASET_FOLDER

    # Check if dataset is complete
    # dataset_complete, series = check_data(dataset_folder)

    # If not complete, offer to download it
    # if not dataset_complete:
    #    offer_download_data(series, dataset_folder)

    # Identify DICOM series & associated ROIs
    dicom_folders_map = identify_images_rois(dataset_folder)

    # Launch conversion & extraction pipeline
    extracted_features_df = run_feature_extraction(dicom_folders_map)

    # Save extracted features to the output folder
    extracted_features_df.to_csv(OUTPUT_FILE_NAME, index=False)

    # Change the file permissions so it's read/write for everyone
    os.chmod(OUTPUT_FILE_NAME, 0o666)
