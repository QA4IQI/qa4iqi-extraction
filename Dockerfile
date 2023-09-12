FROM python:3.10

# Define working directory
WORKDIR /usr/src/app

# Copy pyradiomics parameters
COPY params/qa4iqi_params.yml /data/params/qa4iqi_params.yml

# Copy requirements
COPY requirements.txt /requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Install numpy first (required for pyradiomics)
RUN pip install numpy

# Install requirements
RUN pip install -r /requirements.txt

# Copy source code
COPY qa4iqi_extraction/ qa4iqi_extraction/

# Define default environment variables for log level etc.
RUN echo "LOG_LEVEL=ERROR" > .env

# Run feature extraction by default
CMD ["python", "-m", "qa4iqi_extraction.main"]