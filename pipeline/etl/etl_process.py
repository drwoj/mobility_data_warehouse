import numpy as np
import pandas as pd
from shapely import wkt
import etl.extract.extract as e
import etl.transform.transform as t
import paths as p
import geopandas as gpd
from database.connectors.MobilityDWConnector import MobilityDWConnector

df_weather_hannover = e.extract_weather(p.path_weather_hannover)
df_weather_beijing = e.extract_weather(p.path_weather_beijing)
df_districts_hannover = e.pd.read_excel(p.path_regions, sheet_name='hannover')
df_districts_beijing = e.pd.read_excel(p.path_regions, sheet_name='beijing')
df_fuel_prices_hannover = e.extract_fuel_hannover(p.path_fuel_hannover)
df_fuel_prices_beijing = pd.read_excel(p.path_fuel_beijing,
                                       header=1,
                                       names=['date', 'gasoline', 'diesel'])
df_economy_indicators = e.extract_economy_indicators(p.path_economy)

t.filter_weather_station(df_weather_hannover, 'GME00102244')
df_weather_hannover['city'] = 'Hannover'
df_weather_beijing['city'] = 'Beijing'
df_districts_hannover['city'] = 'Hannover'
df_districts_beijing['city'] = 'Beijing'
df_fuel_prices_hannover['city'] = 'Hannover'
df_fuel_prices_beijing['city'] = 'Beijing'

t.country_to_city(df_economy_indicators)
t.extend_year_to_full_date(df_economy_indicators)

df_weather = pd.concat([df_weather_beijing, df_weather_hannover], ignore_index=True)
df_districts = pd.concat([df_districts_beijing, df_districts_hannover], ignore_index=True)
df_fuel_prices = pd.concat([df_fuel_prices_beijing, df_fuel_prices_hannover], ignore_index=True)
df_dates = e.extract_dates()
df_trajectories = e.extract_trajectories()

t.country_to_city(df_trajectories)

df_list = [df_districts, df_weather, df_economy_indicators, df_fuel_prices]
for df in df_list:
    df['id'] = df.index + 1

t.calculate_foreign_key(df_trajectories, df_weather, 'weather', 'day')
t.calculate_foreign_key(df_trajectories, df_fuel_prices, 'fuel_price', 'month')
t.calculate_foreign_key(df_trajectories, df_economy_indicators, 'economy_indicator', 'year')

df_trajectories['center_point'] = df_trajectories['center_point'].apply(wkt.loads)
df_districts['region_polygon'] = df_districts['area'].apply(wkt.loads)
t.find_matching_regions(df_trajectories, df_districts)
t.calculate_date_id(df_trajectories, df_dates)

df_weather.drop(columns=['date', 'station', 'id', 'city'], inplace=True)
df_fuel_prices.drop(columns=['date', 'city', 'id'], inplace=True)
df_economy_indicators.drop(columns=['date', 'city', 'id', 'Population, female', 'Population, male'], inplace=True)

gdf_districts = gpd.GeoDataFrame(df_districts,
                                 geometry=df_districts['region_polygon'],
                                 crs='EPSG:4326') \
    .drop(columns={'area', 'id', 'region_polygon'}, axis=1) \
    .rename(columns={'geometry': 'area'}) \
    .set_geometry('area', crs='EPSG:4326')

df_trajectories = df_trajectories.replace({np.nan: None})

with MobilityDWConnector() as connector:
    connector.insert_df(df_weather, 'weather')
    connector.insert_df(df_fuel_prices, 'fuel_price')
    connector.insert_df(df_economy_indicators, 'economy_indicator')
    connector.insert_gdf(gdf_districts)

    for index, row in df_trajectories.iterrows():
        route_value = row['route']
        if pd.isna(route_value):
            continue
        distance_value = row['distance'] if not pd.isna(row['distance']) else 'NULL'
        duration_value = row['duration'] if not pd.isna(row['duration']) else 'NULL'
        avg_speed_value = row['avg_speed'] if not pd.isna(row['avg_speed']) else 'NULL'
        date_id_value = row['date_id'] if not pd.isna(row['date_id']) else 'NULL'
        weather_id_value = row['weather_id'] if not pd.isna(row['weather_id']) else 'NULL'
        district_id_value = row['district_id'] if not pd.isna(row['district_id']) else 'NULL'
        economy_indicator_id_value = row['economy_indicator_id'] if not pd.isna(row['economy_indicator_id']) else 'NULL'
        fuel_price_id_value = row['fuel_price_id'] if not pd.isna(row['fuel_price_id']) else 'NULL'

        connector.execute_query(f"""
            INSERT INTO trajectory (route, distance, duration, avg_speed, date_id, weather_id, district_id, economy_indicator_id, fuel_price_id)
            VALUES (
                TGeogPoint('{{{route_value}}}'),
                {distance_value},
                '{duration_value}',
                {avg_speed_value},
                {date_id_value},
                {weather_id_value},
                {district_id_value},
                {economy_indicator_id_value},
                {fuel_price_id_value}
            )""")
