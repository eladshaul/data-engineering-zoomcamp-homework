
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
    docker run -it \
  --network=01-docker-terraform_default \
  taxi_ingest:v001 \
  ingest_green_taxi_data.py \
    --pg-user=elad \
    --pg-pass=elad \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=green_taxi_data \
    --url="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"

    docker run -it \
  --network=01-docker-terraform_default \
  taxi_ingest:v001 \
  ingest_taxi_zone.py \
    --pg-user=elad \
    --pg-pass=elad \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=taxi_zones \
    --chunksize=250
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"



## Question 3:

**Answer:** The correct answer is 8007.

select count(*) from 
public.green_taxi_data a
left join
public.taxi_zones b
on a."PULocationID" = b."LocationID"
where trip_distance <= 1
and EXTRACT(MONTH FROM  "lpep_pickup_datetime") = 11
and EXTRACT(YEAR FROM  "lpep_pickup_datetime") = 2025

## Question 4:

**Answer:** The correct answer is 2025-11-14

select  CAST(lpep_pickup_datetime AS DATE) AS  "DATE",  max(trip_distance) AS "MAX_DATE"
from 
public.green_taxi_data a
left join
public.taxi_zones b
on a."PULocationID" = b."LocationID"
where trip_distance < 100
group by CAST(lpep_pickup_datetime AS DATE)
ORDER BY  "MAX_DATE" DESC


## Question 5:

**Answer:** The correct answer is East Harlem North

select b."Zone", sum(total_amount) "sum_total_amount" 
from 
public.green_taxi_data a
left join
public.taxi_zones b
on a."PULocationID" = b."LocationID"
where 1=1
and EXTRACT(MONTH FROM  "lpep_pickup_datetime") = 11
and EXTRACT(YEAR FROM  "lpep_pickup_datetime") = 2025
and EXTRACT(day FROM  "lpep_pickup_datetime") = 18
group by b."Zone"
order by "sum_total_amount" desc


## Question 6:

**Answer:** The correct answer is Yorkville West

select c."Zone", max(tip_amount) "max_tip" 
from 
public.green_taxi_data a
left join
public.taxi_zones b
on a."PULocationID" = b."LocationID"
left join
public.taxi_zones c
on a."DOLocationID" = c."LocationID"
where 1=1
and EXTRACT(MONTH FROM  "lpep_pickup_datetime") = 11
and EXTRACT(YEAR FROM  "lpep_pickup_datetime") = 2025
and b."Zone" = 'East Harlem North'
group by c."Zone"
order by "max_tip" desc

