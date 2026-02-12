# Data Engineering Zoomcamp 2026 - Module 3 Homework

This repository contains the solution for the third module of the Data Engineering Zoomcamp. The project focuses on working with BigQuery and Google Cloud Storage.


## Infrastructure Setup - load the data into GCS bucket

The following Python script automates the process of downloading the Yellow Taxi Parquet files (Jan-Jun 2024) and uploading them directly to a GCS bucket.

[upload_files.py](upload_files.py)

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

**Answer:** is **False**.

Somtimes cluster is not the best practice because it is not efficient :
1. Table Size < 1GB
2. Clusterin is not efficient in a table with big amount of updating data.
3. Cluster only efficient on the columns you order or filter.
4. Not the best practics on Staging tables. 

***

## Question 9:  

**Answer:** is **0 B**.

BigQuery using the Metadata of the table rather then scan the data.
