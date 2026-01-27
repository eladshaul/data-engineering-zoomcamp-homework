
import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm



@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
@click.option('--url', help='URL of the parquet file')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, url):


    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df = pd.read_parquet(url)

    first = True

    df.head(0).to_sql(name=target_table,con=engine,if_exists="replace")
    
    df.to_sql(name=target_table,con=engine,if_exists="append")

    print("Inserted:", len(df))


if __name__== '__main__':

    run()
