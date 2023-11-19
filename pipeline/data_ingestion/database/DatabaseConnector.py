import os
import geopandas as gpd
from geoalchemy2 import Geography
from sqlalchemy import create_engine
import configparser


class DatabaseConnector:
    _instance = None

    def __init__(self, config_file='config.ini'):
        self.engine = None
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        return cls._instance

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        db_params = {
            'host': config['database']['host'],
            'port': config['database']['port'],
            'database': config['database']['database'],
            'user': config['database']['user'],
            'password': config['database']['password'],
        }
        return db_params

    def connect(self):
        db_params = self.read_config()
        self.engine = create_engine(
            f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@"
            f"{db_params['host']}:{db_params['port']}/{db_params['database']}")

    def insert_gdf(self, gdf: gpd.GeoDataFrame):
        print("Begin Load")
        gdf.to_postgis('point', self.engine, if_exists='append', index=False,
                       schema='public', dtype={'coordinates': Geography('POINT', srid='4326')})
        print("Loading Finished!")

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
