from geoalchemy2 import Geography
import geopandas as gpd

from database.connectors.GenericDatabaseConnector import GenericDatabaseConnector


class MobilityDWConnector(GenericDatabaseConnector):
    def __init__(self, section='database_mobility_dw'):
        super().__init__(section)

    def insert_gdf(self, gdf: gpd.GeoDataFrame):
        print("Begin Load")
        gdf.to_postgis('district',
                       self.engine,
                       if_exists='append',
                       index=False,
                       schema='public',
                       dtype={'area': Geography('MULTIPOLYGON', srid='4326')})
        print("Loading Finished")
