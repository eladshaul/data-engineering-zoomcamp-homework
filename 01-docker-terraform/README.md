
## Question 1: 

**Command executed:**
# bash

docker run -it --entrypoint=bash --rm python:3.13

**Inside the container:**
# bash

pip --version

**Answer:**
The version of pip is **25.3**.



## Question 2:

**Answer:** The correct hostname and port are **db:5432**.

**Reasoning:**
- **Hostname:** In a Docker Compose network, services communicate using the service name defined in the YAML file (in this case, `db`). 
- **Port:** Since `pgadmin` and `db` are in the same network, they communicate via the container's internal port (`5432`).



## Question 3:

**Download Data Sets**

# bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv


**install Python package and project manager - UV**
# bash
pip install uv

**initialize a Python project with uv**
# bash
uv init --python=3.13

**Checking Python Versions in the virtual environment**
# bash
uv run which python
uv run python -V

**Adding Dependencies**
# bash
uv add pandas pyarrow tqdm click
uv add sqlalchemy psycopg2-binary

**Adding dev Dependencies**
# bash
uv add --dev pgcli
uv add --dev jupyter


**Create data ingesttion script file**

    # bash
    uv run jupyter notebook

  ***Data sets exploration***
    # bash
    uv run jupyter nbconvert --to=script data_exploration.ipynb

    # Attached  - data_exploration.py

  ***Creating Data ingestion scripts***

    # Attached  - ingest_green_taxi_data.py
    # Attached  - ingest_taxi_zone.py

  ***Creating dockerfile to creat docker image for data pipeline ingestion***

    # Attached - Dockerfile

  ***Build***
    #bash
    docker build -t taxi_ingest:v001 .

  ***Creating docker-compose to launch Postgres and PgAdmin containers***
    
    ***Creating virtual Docker network***
    #bash
    docker network create pg-network

    # Attached - docker-compose.yaml

   ***Run Docker-compose***
  #bash 
  docker-compose up

  ***Run the Containerized Ingestionn***
    
    #bash


    docker run -it taxi_ingest:v001 \
    ingest_green_taxi_data.py \
        --pg-user=elad \
        --pg-pass=elad \
        --pg-host=pgdatabase \
        --pg-port=5432 \
        --pg-db=ny_taxi \
        --target-table=taxi_zones \
        --url=""


