import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta
from shapely.geometry import Point
import shapely.wkt


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


def is_point_in_polygon(latitude, longitude, polygon):
    point = Point(longitude, latitude)
    return polygon.contains(point)


def is_in_beijing(df):
    beijing_wkt = 'POLYGON((116.366634206204 40.94720525696366, 115.7920922061627 40.58849435745945, 115.448785056998 40.04268727176074, 115.4402477617167 39.72897214234753, 115.5338138630918 39.58376171860291, 115.7598968223046 39.50043355715104, 116.4595889684596 39.43645949786928, 116.5285872023119 39.5549668886424, 116.8399893020106 39.61438608671229, 117.3935747118923 40.17697925101756, 117.5214386135323 40.67500019558564, 116.6788483158374 41.06392405632585, 116.366634206204 40.94720525696366))'
    beijing_polygon = shapely.wkt.loads(beijing_wkt)
    return all(is_point_in_polygon(row.latitude, row.longitude, beijing_polygon) for row in df.itertuples(index=False))
