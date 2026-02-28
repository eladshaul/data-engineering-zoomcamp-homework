"""@bruin

name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: When the meter was engaged
  - name: dropoff_datetime
    type: timestamp
    description: When the meter was disengaged
  - name: pickup_location_id
    type: integer
    description: Pickup location ID
  - name: dropoff_location_id
    type: integer
    description: Dropoff location ID
  - name: fare_amount
    type: float
    description: Base fare amount
  - name: taxi_type
    type: string
    description: Type of taxi (yellow, green, etc.)
  - name: payment_type
    type: integer
    description: Payment type ID

@bruin"""

import os
import json
import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

def materialize():
    """
    Fetch NYC Taxi data from TLC public endpoint and return as DataFrame.
    
    Required Bruin concepts to use here:
    - Built-in date window variables:
      - BRUIN_START_DATE / BRUIN_END_DATE (YYYY-MM-DD)
      - BRUIN_START_DATETIME / BRUIN_END_DATETIME (ISO datetime)
    - Pipeline variables:
      - Read JSON from BRUIN_VARS, e.g. `taxi_types`
    
    Design:
    - Use start/end dates + `taxi_types` to generate a list of source endpoints for the run window.
    - Fetch data for each endpoint, parse into DataFrames, and concatenate.
    - Add a column like `extracted_at` for lineage/debugging (timestamp of extraction).
    - Prefer append-only in ingestion; handle duplicates in staging.
    """
    
    # Get environment variables
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    # Parse dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Generate list of months between start and end dates
    months = []
    current = start
    while current <= end:
        months.append((current.year, current.month))
        current += relativedelta(months=1)

    # Fetch parquet files from TLC endpoint
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    dfs = []

    for taxi_type in taxi_types:
        for year, month in months:
            file_name = f"{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
            url = f"{base_url}{file_name}"
            
            try:
                print(f"Fetching {url}...")
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Read parquet from bytes
                df = pd.read_parquet(pd.io.common.BytesIO(response.content))
                
                # Add taxi_type column to identify the source
                df['taxi_type'] = taxi_type
                
                dfs.append(df)
                print(f"Successfully loaded {file_name} ({len(df)} rows)")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {file_name}: {e}")
                continue
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                continue

    if not dfs:
        raise ValueError(f"No data fetched for taxi types {taxi_types} between {start_date} and {end_date}")

    # Combine all dataframes
    final_dataframe = pd.concat(dfs, ignore_index=True)
    print(f"Total rows loaded: {len(final_dataframe)}")
    
    return final_dataframe