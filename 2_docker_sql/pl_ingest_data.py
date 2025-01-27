#!/usr/bin/env python
# coding: utf-8

import argparse

import os

import pandas as pd 

import polars as pl

import sqlalchemy as sql

import sys

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

    os.system(f"wget {url} -O {csv_name}")

    df = pl.read_csv(csv_name)

    df = df.with_columns(pl.col("tpep_pickup_datetime", "tpep_dropoff_datetime").str.to_datetime("%Y-%m-%d %H:%M:%S"))

    uri = "postgresql://{user}:{password}@{host}:{port}/{db}"
 
    df.write_database(table_name=table_name,  connection=uri)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)