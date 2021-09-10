# qa4iqi-extraction
Code for QA4IQI Radiomics Feature Extraction

1. To build this container from source, navigate to this directory and run:
docker build -t pyradiomics .

2. Run new container from created image
docker run -it --rm -v ~/dicomPhantomScans:/home/jovyan/data/newData -v ~/dockerbuild/qa4iqi:/home/jovyan/qa4iqi pyradiomics python runPipeline.py

* The output pyRadiomics features will be stored in the mounted volume ~/dockerbuild/qa4iqi, in the directory 'out_radiomics/' as a .csv file.
