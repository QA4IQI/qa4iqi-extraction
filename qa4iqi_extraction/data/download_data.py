import sys
import logging
import inquirer

from functools import reduce
from tcia_utils import nbia
from tqdm import tqdm

logger = logging.getLogger()


def offer_download_data(series, dataset_folder):
    data_size = reduce(lambda s1, s2: s1 + s2["FileSize"], series, 0)
    data_size_gb = data_size / 1024 / 1024 / 1024

    question = [
        inquirer.Confirm(
            "download",
            message=(
                f"Dataset is non-existent or incomplete, would you like to "
                f"download it? The total size of the dataset is {data_size_gb:.2f}GB"
            ),
            default=True,
        )
    ]

    answer = inquirer.prompt(question)

    if answer["download"]:
        download_data(series, dataset_folder)
    else:
        logger.error("Cannot proceed without the dataset.")
        sys.exit(1)


def download_data(series, path):
    logger.info("Downloading the dataset now...")

    progress = tqdm(series)

    for s in progress:
        nbia.downloadSeries([s], path=path)
