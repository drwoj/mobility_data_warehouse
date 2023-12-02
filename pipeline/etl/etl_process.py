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
t.calculate_foreign_key(df_trajectories, df_fuel_prices, 'fuel_prices', 'month')
t.calculate_foreign_key(df_trajectories, df_economy_indicators, 'economy_indicator', 'year')

df_trajectories['center_point'] = df_trajectories['center_point'].apply(wkt.loads)
df_districts['region_polygon'] = df_districts['area'].apply(wkt.loads)
t.find_matching_regions(df_trajectories, df_districts)
t.calculate_date_id(df_trajectories, df_dates)

df_weather.drop(columns=['date', 'station', 'id', 'city'], inplace=True)
df_fuel_prices.drop(columns=['date', 'city', 'id'], inplace=True)
df_economy_indicators.drop(columns=['date', 'city', 'id', 'Population, female', 'Population, male'], inplace=True)

gdf = gpd.GeoDataFrame(df_districts,
                       geometry=df_districts['region_polygon'],
                       crs='EPSG:4326') \
    .drop(columns={'area', 'id', 'region_polygon'}, axis=1) \
    .rename(columns={'geometry': 'area'}) \
    .set_geometry('area', crs='EPSG:4326')

print(gdf.sample())

with MobilityDWConnector() as connector:
    connector.insert_df(df_weather, 'weather')
    connector.insert_df(df_fuel_prices, 'fuel_price')
    connector.insert_df(df_economy_indicators, 'economy_indicator')
    connector.insert_gdf(gdf)
