import geopandas as gpd
from geoalchemy2 import Geography
from database.connectors.GenericDatabaseConnector import GenericDatabaseConnector


class StagingAreaConnector(GenericDatabaseConnector):
    def __init__(self, section='database_staging_area'):
        super().__init__(section)

    def insert_gdf(self, gdf: gpd.GeoDataFrame):
        print("Begin Load")
        gdf.to_postgis('point', self.engine,
                       if_exists='append',
                       index=False,
                       schema='public',
                       dtype={'coordinates': Geography('POINT', srid='4326')})
        print("Loading Finished")
