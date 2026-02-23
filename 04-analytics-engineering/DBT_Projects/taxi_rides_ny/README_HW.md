# Data Engineering Zoomcamp 2026 - Module 4 Homework

This repository contains the solution for the fourth module of the Data Engineering Zoomcamp. In this homework, we'll use the dbt project in 04-analytics-engineering/taxi_rides_ny/ to transform NYC taxi data and answer questions by querying the models.



## Question 1: 

**Answer:** If you run `dbt run --select int_trips_unioned`, you run this specific model instead of everything **- `int_trips_unioned` only**.


***

## Question 2: 

**Answer:** When you run `dbt test --select fct_trips` **dbt will fail the test, returning a non-zero exit code**.

The test will fail because the query will retrive at least one row with the value payment_type = 6 

***

## Question 3: 

**Answer:** Count of records in fct_monthly_zone_revenue **12,184**.

```sql
with monthly_zone_revenue as(
select 
        service_type
       ,pickup_location_id 
       ,pickup_zone 
       ,extract(month from pickup_datetime) as pickup_month
       ,extract(year from pickup_datetime) as pickup_year
       ,sum(total_amount)total_amount
       
from {{ref("fct_trips")}}

group by 
        service_type
        ,pickup_location_id 
        ,pickup_zone 
        ,extract(month from pickup_datetime) 
        ,extract(year from pickup_datetime) 

order by 2,4,3
)
select count(*) as 'Count of records' from monthly_zone_revenue
```

***

## Question 4: 

**Answer:** The zone with the highest revenue for Green taxis in 2020  **East Harlem North**.

```sql
with monthly_zone_revenue as(
select 
        service_type
       ,pickup_location_id 
       ,pickup_zone 
       ,sum(total_amount)total_amount
       


from {{ref("fct_trips")}}

where service_type = 'Green'
and extract(year from pickup_datetime) = 2020
group by 
        service_type
        ,pickup_location_id 
        ,pickup_zone 

order by 2,4,3
)
select * from monthly_zone_revenue
order by total_amount desc
```

***


## Question 5: 

**Answer:** The total number of trips for Green taxis in October 2019 **384,624**.


```sql
with monthly_zone_revenue as(
select 
        service_type
       ,pickup_location_id 
       ,pickup_zone 
       ,sum(total_amount) total_amount
       ,count(*) cnt_pickup_location_id
       ,sum(count(*)) over() cnt_total
       


from {{ref("fct_trips")}}

where service_type = 'Green'
and extract(year from pickup_datetime) = 2019
and extract(month from pickup_datetime) = 10
group by 
        service_type
        ,pickup_location_id 
        ,pickup_zone 

order by 2,4,3
)
select * from monthly_zone_revenue
order by total_amount desc
```

***

## Question 6: 

**Answer:** count of records in stg_fhv_tripdata **43,244,693**.

Creating a staging model for the For-Hire Vehicle (FHV) trip data for 2019.

1. Loading the FHV trip data for 2019 into the data warehouse. [ingest_FHV.py](ingest_FHV.py)
2. Creating a staging model stg_fhv_tripdata with these requirements: [stg_fhv_tripdata.sql](stg_fhv_tripdata.sql)
    * Filter out records where `dispatching_base_num IS NULL`
    * rename fields.

```sql
with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),
renamed as (
    select
        -- identifiers
        dispatching_base_num,
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropOff_datetime as timestamp) as dropOff_datetime,
        cast(PUlocationID as integer) as pickup_location_id,
        cast(DOlocationID as integer) as dropoff_location_id,
        SR_Flag,	
        Affiliated_base_number

    from source
    where extract(year from pickup_datetime) = 2019
    and dispatching_base_num IS not NULL
)

select count(*) from renamed
```

***
