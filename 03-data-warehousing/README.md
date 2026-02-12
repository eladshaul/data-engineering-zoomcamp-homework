# Data Engineering Zoomcamp 2026 - Module 3 Homework

This repository contains the solution for the third module of the Data Engineering Zoomcamp. The project focuses on working with BigQuery and Google Cloud Storage.


## Infrastructure Setup - load the data into GCS bucket

```python
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time


# Change this to your bucket name
BUCKET_NAME = "kestra-zoomcamp-elad-demo"

# If you authenticated through the GCP SDK you can comment out these two lines
CREDENTIALS_FILE = "gcs.json"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
# If commented initialize client with the following
# client = storage.Client(project='zoomcamp-mod3-datawarehouse')


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]
DOWNLOAD_DIR = "."

CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)


def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def create_bucket(bucket_name):
    try:
        # Get bucket details
        bucket = client.get_bucket(bucket_name)

        # Check if the bucket belongs to the current project
        project_bucket_ids = [bckt.id for bckt in client.list_buckets()]
        if bucket_name in project_bucket_ids:
            print(
                f"Bucket '{bucket_name}' exists and belongs to your project. Proceeding..."
            )
        else:
            print(
                f"A bucket with the name '{bucket_name}' already exists, but it does not belong to your project."
            )
            sys.exit(1)

    except NotFound:
        # If the bucket doesn't exist, create it
        bucket = client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden:
        # If the request is forbidden, it means the bucket exists but you don't have access to see details
        print(
            f"A bucket with the name '{bucket_name}' exists, but it is not accessible. Bucket name is taken. Please try a different bucket name."
        )
        sys.exit(1)


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    create_bucket(BUCKET_NAME)

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, MONTHS))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, file_paths))  # Remove None values

    print("All files processed and verified.")
    ```

***

## Creating external table referring to gcs path

```sql
CREATE OR REPLACE EXTERNAL TABLE `nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://kestra-zoomcamp-elad-demo/yellow_tripdata_2024-*.parquet']
);
```

## Create a non partitioned table from external table

```sql
CREATE OR REPLACE TABLE nytaxi.yellow_tripdata_non_partitioned01_06_24 AS
SELECT * FROM nytaxi.external_yellow_tripdata;
```



## Question 1: 

**Answer:** The count of records for the Yellow Taxi Data is **20,332,093**.

```sql
SELECT count(*) FROM nytaxi.yellow_tripdata_non_partitioned01_06_24 
```


***

## Question 2: 

**Answer:** The estimated amount of data that will be read is **0 MB for the External Table and 155.12 MB for the Materialized Table**.

```sql
SELECT count(distinct PULocationID) FROM nytaxi.yellow_tripdata_non_partitioned01_06_24 
SELECT count(distinct PULocationID) FROM nytaxi.external_yellow_tripdata
```

***

## Question 3: 

**Answer:**  **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**.

```sql
SELECT  PULocationID FROM nytaxi.yellow_tripdata_non_partitioned01_06_24 
SELECT  PULocationID,DOLocationID FROM nytaxi.yellow_tripdata_non_partitioned01_06_24 
```

***

## Question 4: 

**Answer:** The number of records are **8,333**.

```sql
SELECT  count(*) FROM nytaxi.yellow_tripdata_non_partitioned01_06_24 where fare_amount = 0
```

***


## Question 5: 

**Answer:** The number of records are **Partition by tpep_dropoff_datetime and Cluster on VendorID**.


```sql
CREATE OR REPLACE TABLE nytaxi.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM nytaxi.external_yellow_tripdata;
```

***

## Question 6: 

**Answer:** The number of records are **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**.


```sql
select distinct VendorID
from nytaxi.yellow_tripdata_partitioned_clustered
where tpep_pickup_datetime between  '2024-03-01' and '2024-03-15'

select distinct VendorID
from nytaxi.yellow_tripdata_non_partitioned01_06_24 
where tpep_pickup_datetime between  '2024-03-01' and '2024-03-15'
```

***

## Question 7: 

**Answer:** The number of records are **GCP Bucket**.


***

## Question 8: 

**Answer:** The number of records are ****.


```sql

```

***