# Build the Python app
FROM radiomics/pyradiomics
MAINTAINER Oscar Jimenez

# Set environment variables
USER jovyan

# QA4IQI code
COPY qa4iqi/code/ ./

RUN pip install -r requirements.txt

EXPOSE 80