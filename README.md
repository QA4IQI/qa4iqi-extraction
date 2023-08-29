# qa4iqi-extraction
Code for QA4IQI Radiomics Feature Extraction

1. To build this container from source, navigate to this directory and run:
docker build -t pyradiomics .

2. Run new container from created image
docker run -it --rm -v ~/dicomPhantomScans:/home/jovyan/data/newData -v ~/dockerbuild/qa4iqi:/home/jovyan/qa4iqi pyradiomics python runPipeline.py

* The output pyRadiomics features will be stored in the mounted volume ~/dockerbuild/qa4iqi, in the directory 'out_radiomics/' as a .csv file.

## Reference images
The QA4IQI reference data (used for printing the phantom) can be downloaded here: https://www.dropbox.com/s/yf5cqprkyuxwcwv/refData.zip?dl=0

## Phantom Scans Dataset
The dataset of phantom scans is available on TCIA here : https://doi.org/10.7937/a1v1-rc66
