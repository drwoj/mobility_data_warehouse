import pandas as pd
from shapely import wkt

import paths as p
import geopandas as gpd
from database.connectors.StagingAreaConnector import StagingAreaConnector


def ingest_districts(db):
    df_districts_hannover = pd.read_excel(p.path_regions, sheet_name='hannover')
    df_districts_beijing = pd.read_excel(p.path_regions, sheet_name='beijing')

    df_districts_hannover['city'] = 'Hannover'
    df_districts_beijing['city'] = 'Beijing'
    df_districts = pd.concat([df_districts_beijing, df_districts_hannover], ignore_index=True)

    df_districts['region_polygon'] = df_districts['area'].apply(wkt.loads)
    gdf_districts = gpd.GeoDataFrame(df_districts,
                                         geometry=df_districts['region_polygon'],
                                         crs='EPSG:4326') \
            .drop(columns={'area', 'region_polygon'}, axis=1) \
            .rename(columns={'geometry': 'area'}) \
            .set_geometry('area', crs='EPSG:4326')

    gdf_districts = pd.concat([gdf_districts, pd.DataFrame.from_records([{'name': 'unknown',
                                                                          'city': None,
                                                                          'area': None}])])

    db.insert_gdf(gdf_districts, 'district', 'area', 'MULTIPOLYGON')
