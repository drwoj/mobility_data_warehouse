import os

import pandas as pd
from geoalchemy2 import Geography
from sqlalchemy import create_engine, text
import configparser


class GenericDatabaseConnector:
    _instance = None

    def __init__(self, section='database'):
        self.engine = None
        package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(package_dir, 'config.ini')
        self.section = section

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GenericDatabaseConnector, cls).__new__(cls)
        return cls._instance

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        db_params = {
            'host': config[self.section]['host'],
            'port': config[self.section]['port'],
            'database': config[self.section]['database'],
            'user': config[self.section]['user'],
            'password': config[self.section]['password'],
        }
        return db_params

    def execute_query(self, query):
        with self.engine.begin() as connection:
            statement = text(query)
            connection.execute(statement)

    def execute_select_query(self, query):
        with self.engine.begin() as connection:
            statement = text(query)
            rows = connection.execute(statement)
            df = pd.DataFrame.from_records(rows, columns=rows.keys())
            return df

    def insert_df(self, df, name):
        with self.engine.begin() as connection:
            print("Begin insert")
            df.to_sql(name, con=connection, index=False, if_exists='append')
            print("Insert Finished")

    def truncate_and_restart_identity(self, table_name):
        with self.engine.begin() as connection:
            statement = text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;')
            connection.execute(statement)
            print(f"Table {table_name} cleaned")

    def insert_gdf(self, gdf, table, column, geo_type):
        print("Begin Load")
        gdf.to_postgis(table,
                       self.engine,
                       if_exists='append',
                       index=False,
                       schema='public',
                       dtype={column: Geography(geo_type, srid='4326')})
        print("Loading Finished")

    def connect(self):
        db_params = self.read_config()
        self.engine = create_engine(
            f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@"
            f"{db_params['host']}:{db_params['port']}/{db_params['database']}")

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
