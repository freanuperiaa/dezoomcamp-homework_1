from time import time
import pandas as pd
from sqlalchemy import create_engine
import argparse
import wget


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    # url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    csv_name = 'output.csv'

    # get the csv
    wget.download(url, 'green_tripdata_2019-01.csv.gz')

    # connect to db
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # create an iterator for .csv file
    df_iter = pd.read_csv('green_tripdata_2019-01.csv.gz', compression='gzip', iterator=True, chunksize=100000, low_memory=False)

    df = next(df_iter)

    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # create the table to the postgres db first
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')


    # add the rows to the table in the db
    df.to_sql(name=table_name, con=engine, if_exists='append')



    # insert the rest of the rows in the postgres table

    while True:
        try:
            t_start = time()
        
            df = next(df_iter)
            # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()
            print('inserted another chunk. took %.3f second' % (t_end - t_start))

        except:
            print("error caught. probably done loading")


if __name__ == '__main__':
    # retrieving arguments
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    # user
    # password
    # host
    # port
    # database name
    # table name
    # url of the csv
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write data')
    parser.add_argument('--url', help='url of the csv')

    args = parser.parse_args()

    # url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
    main(args)

