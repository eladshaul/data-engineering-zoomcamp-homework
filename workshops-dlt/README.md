# Data Engineering Zoomcamp 2026 - Workshop - dlt

In this homework, I'll use an AI-powered IDE to build a complete data pipeline from an API to a local data warehouse with dlt (data load tool).

## Set Up the dlt MCP Server in Cursor settings

```json
{
  "mcpServers": {
    "dlt": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "dlt[duckdb]",
        "--with",
        "dlt-mcp[search]",
        "python",
        "-m",
        "dlt_mcp"
      ]
    }
  }
}
```
## Install dlt

```bash
pip install -U "dlt[rest_api]"
```

## Initialize the Project

```bash
dlt init dlthub:taxi_pipeline duckdb
```

## Prompt the Agent

```txt
Build a REST API source for NYC taxi data.

API details:
- Base URL: https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
- Data format: Paginated JSON (1,000 records per page)
- Pagination: Stop when an empty page is returned

Place the code in taxi_pipeline.py and name the pipeline taxi_pipeline.
Use @dlt rest api as a tutorial.` 
```
## Generate python pipeline 

['taxi_pipeline.py'](taxi_pipeline.py)

## Question 1: 

 What is the start date and end date of the dataset? 
 
**2009-06-01 to 2009-07-01**.

```sql
SELECT min(trip_pickup_date_time), max(trip_dropoff_date_time)
FROM "taxi_rides"
```



***

## Question 2: 

What proportion of trips are paid with credit card?

**26.66%**.

```sql
SELECT count(*) as cnt_trips,
       sum(case when payment_type='Credit' then 1 else 0 end) as cnt_credit,
       sum(case when payment_type='Credit'  then 1 else 0 end)/count(*) as pct_credit
FROM "taxi_rides"
```

***

## Question 3: 

What is the total amount of money generated in tips?  

**$6,063.41**.

```sql
SELECT sum(tip_amt) tips_total_amount
FROM "taxi_rides"
```

***
