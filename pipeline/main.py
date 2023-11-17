from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import utm


db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'staging_area',
    'user': 'postgres',
    'password': 'postgres'
}

path_csv = r'C:\Users\drwoj\Desktop\inzynierka\datasets\trajectories_hannover.csv'

df = pd.read_csv(path_csv)
df['north_utm'], df['east_utm'] = utm.to_latlon(df['east_utm'], df['north_utm'], 32, 'N')
df['unixtime'] = pd.to_datetime(df['unixtime'], unit='s')

gdf = gpd.GeoDataFrame(df,
                       geometry=gpd.points_from_xy(df['east_utm'], df['north_utm']),
                       crs="EPSG:5555")

gdf.rename(columns={'trip_id': 'trajectory_id',
                    'unixtime': 'timestamp',
                    'geometry': 'coordinates'}, inplace=True)

gdf.drop(columns={'gid',
                  'east_utm',
                  'north_utm'}, axis=1, inplace=True)

gdf.set_geometry('coordinates', inplace=True, crs="EPSG:5555")
gdf['object_type'] = 'car'
gdf['country'] = 'Germany'

engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}"
                       f"@{db_params['host']}:{db_params['port']}/{db_params['database']}")

print("Begin Load")
gdf.to_postgis('point', engine, if_exists='replace', index=False, schema='public')
print("Loading Finished!")
engine.dispose()
