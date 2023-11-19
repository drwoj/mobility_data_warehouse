import os
import pandas as pd
from prefect import task


def extract_geolife(path_plt):
    path_txt = os.path.splitext(path_plt)[0] + '.txt'
    os.rename(path_plt, path_txt)

    df = pd.read_csv(path_txt,
                     skiprows=6,
                     header=None,
                     usecols=[0, 1, 4],
                     names=['latitude', 'longitude', 'timestamp'])

    os.rename(path_txt, path_plt)
    return df


def extract_hannover(path_csv):
    df = pd.read_csv(path_csv) \
        .rename(columns={'trip_id': 'trajectory_id'})
    return df
