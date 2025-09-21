# Base image
FROM python:3.10-slim

# set working directory
WORKDIR /etl-pipeline-postgres-docker

# copy files from host to container
COPY . /etl-pipeline-postgres-docker

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ,"etl.py" ]