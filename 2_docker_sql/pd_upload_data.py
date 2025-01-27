import pandas as pd
pd.__version__
df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

print(pd.io.sql.get_schema(df, name = 'yellow_taxi_2021_01'))

df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)
df = next(df_iter)
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
len(df)
#convert it later to polars

df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

get_ipython().run_line_magic('time', "df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')")

from time import time

while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
        t_end = time()    
        print('inserted another chunk..., took %.3f second' % (t_end - t_start))

#alternative to pgcli, list tables, change anyway you want
query = """
select *
from pg_catalog.pg_tables
where schemaname != 'pg_catalog' and
schemaname != 'information_schema';
"""
pd.read_sql(query, con=engine)

df-to_sql(name='yellow_tripdata_trip', con=engine, index=False)
# In[ ]:




