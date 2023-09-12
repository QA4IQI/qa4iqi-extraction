import os
import logging

from tcia_utils import nbia
from qa4iqi_extraction.constants import TCIA_COLLECTION_NAME

logger = logging.getLogger()


def check_data(dataset_folder):
    logger.info(f"Getting dataset information for collection '{TCIA_COLLECTION_NAME}'")

    series = nbia.getSeries(collection=TCIA_COLLECTION_NAME)
    series_folders = os.listdir(dataset_folder)
    series_present = [s for s in series if s["SeriesInstanceUID"] in series_folders]

    if len(series) != len(series_present):
        return False, series
    else:
        return True, series
