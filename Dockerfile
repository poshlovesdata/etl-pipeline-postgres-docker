# Base image
FROM python:3.10-slim

# set working directory
WORKDIR /app

# copy files from host to container
COPY . /app

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ,"script/etl.py" ]