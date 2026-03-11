# Data Engineering Zoomcamp 2026 - Module 6 Homework

This repository contains the solution for the sixth module of the Data Engineering Zoomcamp. In this homework, I'll set up PySpark and create Spark sessions,
Read and process Parquet files at scale,Repartition data for optimal performance, Analyze millions of taxi trips with DataFrames and Use Spark UI for monitoring jobs.

Detailed implementation and scripts can be found in the [Jupyter Notebook](./Homework.ipynb).

## Question 1: Install Spark and PySpark

Download raw dataset:

```bash
mkdir -p /home/eladshaul/spark/data/raw/yellow/2025/11
```

```bash
wget -P /home/eladshaul/spark/data/raw/yellow/2025/11 https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
```

```bash
pyspark --version
```

Spark version **version 4.1.1**

---

## Question 2: 

```python
df = spark.read \
    .parquet('data/raw/yellow/2025/11/*')
```

```python
df \
     .repartition(4) \
     .write.parquet('06-batch/pq_yelloew_11_26')
```

```bash
ls -lh /home/eladshaul/spark/data/pq/yellow/2025/11/
```

```bash
(spark) eladshaul@LAPTOP-NH6TPSRN:~/spark/06-batch/pq_yelloew_11_26$ ls -lh
total 98M
-rw-r--r-- 1 eladshaul eladshaul   0 Mar 11 12:20 _SUCCESS
-rw-r--r-- 1 eladshaul eladshaul 25M Mar 11 12:20 part-00000-52d08a53-99f9-4af1-bfa8-783c5aa0bb9f-c000.snappy.parquet
-rw-r--r-- 1 eladshaul eladshaul 25M Mar 11 12:20 part-00001-52d08a53-99f9-4af1-bfa8-783c5aa0bb9f-c000.snappy.parquet
-rw-r--r-- 1 eladshaul eladshaul 25M Mar 11 12:20 part-00002-52d08a53-99f9-4af1-bfa8-783c5aa0bb9f-c000.snappy.parquet
-rw-r--r-- 1 eladshaul eladshaul 25M Mar 11 12:20 part-00003-52d08a53-99f9-4af1-bfa8-783c5aa0bb9f-c000.snappy.parquet
```

The average size of the Parquet file to each partition is **25MB**

---

## Question 3: 


```python
df.registerTempTable('df')
```

```python
df_result = spark.sql("""
SELECT to_date(tpep_pickup_datetime) as Date,
        count(1) as cnt
        
FROM df
WHERE to_date(tpep_pickup_datetime)= '2025-11-15'
GROUP BY to_date(tpep_pickup_datetime) 
    LIMIT 1
""")
```

Total trips for Nov 15th: **162,604**

---

## Question 4: 

```python
df_result = spark.sql("""
SELECT 
--    tpep_pickup_datetime, 
--    tpep_dropoff_datetime,
    max((unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 3600) as duration_hours
FROM df
LIMIT 1
""")

df_result.show()
```

The length of the longest trip in the dataset in hours is 

**90.6**

---

## Question 5: 

The Spark User Interface runs on local port 4040 by default. It provides a web dashboard to monitor the status and resource consumption of the Spark application.

**4040**

---

## Question 6: 

```python
zones = spark.read \
    .option("header", "true") \
    .csv('taxi_zone_lookup.csv')
```

```python
df_join = df.join(zones,df.PULocationID == zones.LocationID)
```

```python
df_join \
    .repartition(4) \
    .write.parquet('06-batch/reports/pq_yellow_11_26_with_zones', mode='overwrite')
```

```python
df_join_z = spark.read.parquet('06-batch/reports/pq_yellow_11_26_with_zones/*')
```

```python
df_join_z.registerTempTable('df_join_z')
```
```python
df_join_z = spark.sql("""
SELECT PULocationID  , Zone,
   count(*) as cnt_trips
FROM df_join_z
GROUP BY PULocationID , Borough , Zone
order by cnt_trips ,PULocationID  , Zone 
""")

df_join_z.show()
```

The zone with the least frequent pickup trips is **Arden Heights**