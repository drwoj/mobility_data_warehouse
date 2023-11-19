import os
from datetime import timedelta
from data_ingestion.extract.extract import extract_geolife
from data_ingestion.transform import transform as t
from prefect import task, flow

trajectory_id = 1204  # num of trajectories in hannover


@flow(name="iterate_geolife_dataset")
def iterate_geolife_dataset(db):
    global trajectory_id
    data_folder = r"C:\Users\drwoj\Desktop\inzynierka\datasets\trajectories_china\Geolife Trajectories 1.3\Data"

    for user_folder in os.listdir(data_folder):
        user_path = os.path.join(data_folder, user_folder)
        trajectory_folder = os.path.join(user_path, "Trajectory")

        if os.path.exists(trajectory_folder) and os.path.isdir(trajectory_folder):
            for plt_file in os.listdir(trajectory_folder):
                if plt_file.endswith(".plt"):
                    plt_path = os.path.join(trajectory_folder, plt_file)
                    ingest_geolife(db, plt_path)
                    trajectory_id += 1


@task(name="ingest_geolife_dataset")
def ingest_geolife(db, path):
    global trajectory_id
    path = path
    pause_threshold = timedelta(minutes=1)  # Adjust the threshold as needed

    df = extract_geolife(path)
    df = t.get_df_with_trajectory_id_column(df, trajectory_id)
    df = t.get_df_with_country_column(df, 'China')
    df['timestamp'] = df['timestamp'].apply(t.tdatetime_to_datetime)
    df['time_diff'] = df['timestamp'].diff()

    for i in range(1, len(df)):
        if df['time_diff'][i] > pause_threshold:
            trajectory_id += 1
        df.at[i, 'trajectory_id'] = trajectory_id

    df.drop(columns=['time_diff'], inplace=True)
    gdf = t.get_gdf_with_point_column(df)

    db.insert_gdf(gdf)
