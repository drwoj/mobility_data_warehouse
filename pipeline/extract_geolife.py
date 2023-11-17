from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import os

# data_folder = r"C:\Users\drwoj\Desktop\inzynierka\datasets\trajectories_china\Geolife Trajectories 1.3\Data"
"""
for user_folder in os.listdir(data_folder):
    user_path = os.path.join(data_folder, user_folder)
    trajectory_folder = os.path.join(user_path, "Trajectory")

    if os.path.exists(trajectory_folder) and os.path.isdir(trajectory_folder):
        for plt_file in os.listdir(trajectory_folder):
            if plt_file.endswith(".plt"):
                plt_path = os.path.join(trajectory_folder, plt_file)
                # Perform ETL operations on plt_path
                print(f"Processing file: {plt_path}")
                # Add your ETL code here
"""


def extract(path_plt):
    path_txt = os.path.splitext(path_plt)[0] + '.txt'
    os.rename(path_plt, path_txt)

    df = pd.read_csv(path_txt,
                     skiprows=6,
                     header=None,
                     usecols=[0, 1, 4],
                     names=['latitude', 'longitude', 'timestamp'])

    os.rename(path_txt, path_plt)
    return df


def transform_with_type():
    pass


def transform():
    pass


path = r"C:\Users\drwoj\Desktop\20081218004559.plt"
df = extract(path)
print(df.head(5))
