#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # Download the file
    os.system(f"wget {url} -O {csv_name}")

    # Properly interpolate connection string
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print(f"Engine created successfully!")

    # Read and ingest data in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Create the table if not exists, replace the schema
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    while True:
        try:
            t_start = time()
            
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

            t_end = time()

            print('Inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the Postgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='User name for Postgres')
    parser.add_argument('--password', required=True, help='Password for Postgres')
    parser.add_argument('--host', required=True, help='Host for Postgres')
    parser.add_argument('--port', required=True, help='Port for Postgres')
    parser.add_argument('--db', required=True, help='Database name for Postgres')
    parser.add_argument('--table_name', required=True, help='Name of the table to write the results to')
    parser.add_argument('--url', required=True, help='URL of the CSV file')

    args = parser.parse_args()

    main(args)
