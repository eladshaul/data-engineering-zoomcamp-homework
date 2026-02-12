# Data Engineering Zoomcamp 2026 - Module 3 Homework

This repository contains the solution for the third module of the Data Engineering Zoomcamp. The project focuses on working with BigQuery and Google Cloud Storage.

## Infrastructure Setup

**Creating docker-compose**

1.Installing Kestra
2.PgAdmin
3.Postgres database

```YAML
volumes:
  ny_taxi_postgres_data:
    driver: local
  kestra_postgres_data:
    driver: local
  kestra_data:
    driver: local

services:
  pgdatabase:
    image: postgres:18
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: ny_taxi
    ports:
      - "5432:5432"
    volumes:
      - ny_taxi_postgres_data:/var/lib/postgresql
    depends_on:
      kestra:
        condition: service_started

  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8085:80"
    depends_on:
      pgdatabase:
        condition: service_started

  kestra_postgres:
    image: postgres:18
    volumes:
      - kestra_postgres_data:/var/lib/postgresql
    environment:
      POSTGRES_DB: kestra
      POSTGRES_USER: kestra
      POSTGRES_PASSWORD: k3str4
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 10

  kestra:
    image: kestra/kestra:v1.1
    pull_policy: always
    user: "root"
    command: server standalone
    volumes:
      - kestra_data:/app/storage
      - /var/run/docker.sock:/var/run/docker.sock
      - /tmp/kestra-wd:/tmp/kestra-wd
    env_file: .env_encoded  
    environment:
      KESTRA_CONFIGURATION: |
        datasources:
          postgres:
            url: jdbc:postgresql://kestra_postgres:5432/kestra
            driverClassName: org.postgresql.Driver
            username: kestra
            password: k3str4
        kestra:
          server:
            basicAuth:
              username: "admin@kestra.io" # it must be a valid email address
              password: Admin1234!
          repository:
            type: postgres
          storage:
            type: local
            local:
              basePath: "/app/storage"
          queue:
            type: postgres
          tasks:
            tmpDir:
              path: /tmp/kestra-wd/tmp
          url: http://localhost:8080/
    ports:
      - "8080:8080"
      - "8081:8081"
    depends_on:
      kestra_postgres:
        condition: service_started
    
```


**Add Service Account as a Secret**

Encoding GCP credentionals using base64

```bash
echo SECRET_GCP_SERVICE_ACCOUNT=$(cat service-account.json | base64 -w 0) >> .env_encoded
```

Set the env_encoded file inside of your docker-compose.yml:

```yaml
kestra:
  env_file: .env_encoded
```

**Running the containers**

```bash
cd 02-workflow-orchestration
docker compose up -d
```

**Seting up GCP KV**

```YAML
id: 06_gcp_kv
namespace: zoomcamp

tasks:
  - id: gcp_project_id
    type: io.kestra.plugin.core.kv.Set
    key: GCP_PROJECT_ID
    kvType: STRING
    value: project-ac733521-06f8-46e1-91a
  - id: gcp_location

    type: io.kestra.plugin.core.kv.Set
    key: GCP_LOCATION
    kvType: STRING
    value: europe-west2

  - id: gcp_bucket_name
    type: io.kestra.plugin.core.kv.Set
    key: GCP_BUCKET_NAME
    kvType: STRING
    value: kestra-zoomcamp-elad-demo 

  - id: gcp_dataset
    type: io.kestra.plugin.core.kv.Set
    key: GCP_DATASET
    kvType: STRING
    value: zoomcamp
```

**Creating GCS bucket and BigQuery dataset**

```Yaml
id: 07_gcp_setup
namespace: zoomcamp

tasks:
  - id: create_gcs_bucket
    type: io.kestra.plugin.gcp.gcs.CreateBucket
    ifExists: SKIP
    storageClass: REGIONAL
    name: "{{kv('GCP_BUCKET_NAME')}}" 

  - id: create_bq_dataset
    type: io.kestra.plugin.gcp.bigquery.CreateDataset
    name: "{{kv('GCP_DATASET')}}"
    ifExists: SKIP

pluginDefaults:
  - type: io.kestra.plugin.gcp
    values:
      serviceAccount: "{{secret('GCP_SERVICE_ACCOUNT')}}"
      projectId: "{{kv('GCP_PROJECT_ID')}}"
      location: "{{kv('GCP_LOCATION')}}"
      bucket: "{{kv('GCP_BUCKET_NAME')}}"
```

***

## Question 1: 

**Answer:** The uncompressed file size of yellow_tripdata_2020-12.csv is **134.5 MiB**.

Execute flow in Kestra

[gcp_taxi.yaml](./gcp_taxi.yaml)


***

## Question 2: 

**Answer:** The rendered value is **green_tripdata_2020-04.csv**.

According to this part of the flow cod, 
The value of :
1. inputs.taxi is green.
2. inputs.year is 2020.
3. inputs.month is 04.

The foramat is  {{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv

```YAML
inputs:
  - id: taxi
    type: SELECT
    displayName: Select taxi type
    values: [yellow, green]
    defaults: green

  - id: year
    type: SELECT
    displayName: Select year
    values: ["2019", "2020"]
    defaults: "2019"
    allowCustomValue: true # allows you to type 2021 from the UI for the homework 🤗

  - id: month
    type: SELECT
    displayName: Select month
    values: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    defaults: "01"

variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
  gcs_file: "gs://{{kv('GCP_BUCKET_NAME')}}/{{vars.file}}"
  table: "{{kv('GCP_DATASET')}}.{{inputs.taxi}}_tripdata_{{inputs.year}}_{{inputs.month}}"
  data: "{{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv']}}"
  ```

***

## Question 3: 

**Answer:** The number of rows for the Yellow Taxi data for all CSV files in the year 2020 are **24,648,499**.

Truncate old data from table

```sql
truncate table `project-ac733521-06f8-46e1-91a.zoomcamp.yellow_tripdata` 
```

Execute flow in Kestra

[gcp_taxi_sch.yaml](./gcp_taxi_sch.yaml)

Run Query in BigQuey

```sql
SELECT count(*) FROM `project-ac733521-06f8-46e1-91a.zoomcamp.yellow_tripdata` 
```


***

## Question 4: 

**Answer:** The number of rows for the Green Taxi data for all CSV files in the year 2020 are **1,734,051**.

Truncate old data from table

```sql
truncate table `project-ac733521-06f8-46e1-91a.zoomcamp.green_tripdata` 
```

Execute flow in Kestra

[gcp_taxi_sch.yaml](./gcp_taxi_sch.yaml)

Run Query in BigQuey

```sql
SELECT count(*) FROM `project-ac733521-06f8-46e1-91a.zoomcamp.green_tripdata` 
```

***

## Question 5: 

**Answer:** The correct hostname and port are **1,925,152**.

Execute flow in Kestra

[gcp_taxi_inc_21.yaml](./gcp_taxi_inc_21.yaml)

Run Query in BigQuey

```sql
SELECT count(*) FROM `project-ac733521-06f8-46e1-91a.zoomcamp.yellow_tripdata_2021_03` 
```

***

## Question 6: 

**Answer:** **Add a timezone property set to UTC-5 in the Schedule trigger configuration**.

```YAML
triggers:
  - id: daily_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    timezone: America/New_York
```