import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta


def get_gdf_with_point_column(df: pd.DataFrame):

    invalid_rows = find_rows_with_invalid_coordinates(df)

    if not invalid_rows.empty:
        df = df[~df.index.isin(invalid_rows.index)]

    gdf = gpd.GeoDataFrame(df,
                           geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
                           crs='EPSG:4326') \
        .rename(columns={'geometry': 'coordinates'}) \
        .set_geometry('coordinates', crs='EPSG:4326') \
        .drop(columns={'latitude', 'longitude'}, axis=1)
    return gdf


def find_rows_with_invalid_coordinates(df: pd.DataFrame):
    invalid_rows = (
        (df['longitude'] < -180) | (df['longitude'] > 180) |
        (df['latitude'] < -90) | (df['latitude'] > 90)
    )
    return df[invalid_rows]


def tdatetime_to_datetime(tdatetime):
    base_date = datetime(1899, 12, 30)
    delta = timedelta(days=tdatetime)
    result_datetime = base_date + delta
    return result_datetime.replace(microsecond=0)


def get_df_with_country_column(df: pd.DataFrame, country):
    df.insert(2, 'country', country)
    return df


def filter_rows_with_time_diff_0(df: pd.DataFrame):
    df['time_diff'] = df['timestamp'].diff().fillna(timedelta(seconds=1))
    df = df[df['time_diff'] != timedelta(seconds=0)]
    df = df.reset_index(drop=True)
    return df


def get_df_with_trajectory_id_column(df: pd.DataFrame, trajectory_id):
    df.insert(0, 'trajectory_id', trajectory_id)
    return df
