import dlt
from dlt.sources.rest_api import rest_api_source

def nyc_taxi_pipeline():
    source = rest_api_source(
        {
            "client": {
                "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
            },
            "resources": [
                {
                    "name": "taxi_rides",
                    "endpoint": {
                        "path": "data_engineering_zoomcamp_api",
                        "params": {
                            "page": 1,
                        },
                        "paginator": {
                            "type": "page_number",
                            "base_page": 1,         # API starts at page=1
                            "page_param": "page",
                            "total_path": None,     # No total count in response
                            "stop_after_empty_page": True,  # Stop when API returns []
                        },
                    },
                    "write_disposition": "replace",  # Full reload each run
                },
            ],
        }
    )

    pipeline = dlt.pipeline(
        pipeline_name="nyc_taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data",
    )

    load_info = pipeline.run(
        source,
        loader_file_format="parquet",  # Faster than default jsonl for bulk loads
        write_disposition="replace",
    )

    return load_info


if __name__ == "__main__":
    print("Starting pipeline...")
    info = nyc_taxi_pipeline()
    print(info)

    # Quick row count check
    import duckdb
    conn = duckdb.connect("nyc_taxi_pipeline.duckdb")
    count = conn.sql("SELECT COUNT(*) FROM nyc_taxi_data.taxi_rides").fetchone()[0]
    print(f"\nLoaded {count:,} rows into DuckDB")
    conn.close()