import pandas as pd
import utm
from prefect import task
from data_ingestion.extract.extract import extract_hannover
from data_ingestion.transform import transform as t
from paths import path_trajectories_hannover


@task(name="ingest_hannover_dataset")
def ingest_hannover(db):

    df = extract_hannover(path_trajectories_hannover)
    df['latitude'], df['longitude'] = utm.to_latlon(df['east_utm'], df['north_utm'], 32, 'N')
    df = t.get_df_with_country_column(df, 'Germany')
    df['timestamp'] = pd.to_datetime(df['unixtime'], unit='s')
    df = t.filter_rows_with_time_diff_0(df)
    df.drop(columns=['time_diff'], inplace=True)
    gdf = t.get_gdf_with_point_column(df) \
        .drop(columns={'gid', 'east_utm', 'north_utm', 'unixtime'}, axis=1)

    db.insert_gdf(gdf, 'point', 'coordinates', 'POINT')
