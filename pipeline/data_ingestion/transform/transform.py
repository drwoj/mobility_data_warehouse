import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta


def get_gdf_with_point_column(df: pd.DataFrame):
    gdf = gpd.GeoDataFrame(df,
                           geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
                           crs='EPSG:4326') \
        .rename(columns={'geometry': 'coordinates'}) \
        .set_geometry('coordinates', crs='EPSG:4326') \
        .drop(columns={'latitude', 'longitude'}, axis=1)
    return gdf


def tdatetime_to_datetime(tdatetime):
    base_date = datetime(1899, 12, 30)
    delta = timedelta(days=tdatetime)
    result_datetime = base_date + delta
    return result_datetime.replace(microsecond=0)


def get_df_with_country_column(df: pd.DataFrame, country):
    df.insert(2, 'country', country)

    return df


def get_df_with_trajectory_id_column(df: pd.DataFrame, trajectory_id):
    df.insert(0, 'trajectory_id', trajectory_id)
    return df
