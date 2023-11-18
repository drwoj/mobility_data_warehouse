from extract.extract import extract_geolife
import transform.transform as t

trajectory_id = 1204  # num of trajectories in hannover
data_folder = r"C:\Users\drwoj\Desktop\inzynierka\datasets\trajectories_china\Geolife Trajectories 1.3\Data"
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

def ingest_geolife(db):
    path = r"C:\Users\drwoj\Desktop\20081218004559.plt"
    df = extract_geolife(path)
    df = t.get_df_with_trajectory_id_column(df, trajectory_id)
    df = t.get_df_with_country_column(df, 'China')
    df['timestamp'] = df['timestamp'].apply(t.tdatetime_to_datetime)
    gdf = t.get_gdf_with_point_column(df)

    db.insert_gdf(gdf)

