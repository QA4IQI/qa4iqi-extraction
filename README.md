# qa4iqi-extraction

## Code for QA4IQI Radiomics Feature Extraction

1. To build this container from source, navigate to this directory and run:

   ```
   docker build -t qa4iqi-extraction:latest .
   ```

2. Run a container using the created image

   ```
   docker run -it --rm -v <PATH_TO_DATASET_FOLDER>:/data/ct-phantom4radiomics -v <PATH_TO_OUTPUT_FOLDER>:/data/output qa4iqi-extraction:latest
   ```

   Where:
   - ```<PATH_TO_DATASET_FOLDER>``` is an empty folder on your local hard drive where the dataset will be downloaded to. Make sure to have enough space available on your hard drive, as the full dataset is ~42GB.
   - ```<PATH_TO_OUTPUT_FOLDER>``` is an empty folder on your local hard drive where the extracted features will be saved in a file called **features.csv**.

## Phantom Scans Dataset

The dataset of phantom scans is available on TCIA here: https://doi.org/10.7937/a1v1-rc66

If you publish any work which uses this dataset, please cite the following publication :

> *Schaer, R., Bach, M., Obmann, M., Flouris, K., Konukoglu, E., Stieltjes, B., Müller, H., Aberle, C., Jimenez del Toro, O. A., & Depeursinge, A. (2023). Task-Based Anthropomorphic CT Phantom for Radiomics Stability and Discriminatory Power Analyses (CT-Phantom4Radiomics)*

## Reference images

The QA4IQI reference data (used for printing the phantom) can be downloaded here: https://www.dropbox.com/s/yf5cqprkyuxwcwv/refData.zip?dl=0