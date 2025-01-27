FROM python:3.13

RUN apt-get install wget
RUN pip install pandas polars-lts-cpu sqlalchemy==1.3.9 psycopg2-binary psycopg2 argparse

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]