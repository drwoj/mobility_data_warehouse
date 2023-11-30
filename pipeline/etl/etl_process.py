import pandas as pd

import etl.extract.extract as e
import etl.transform.transform as t
import paths as p
pd.set_option('display.max_columns', None)


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

df_trajectories = e.extract_trajectories()
t.add_foreign_key_columns(df_trajectories)
t.country_to_city(df_trajectories)

df_list = [df_districts, df_weather, df_economy_indicators, df_fuel_prices]
for df in df_list:
    df['id'] = df.index

t.calculate_foreign_key(df_trajectories, df_weather, 'weather', 'day')
t.calculate_foreign_key(df_trajectories, df_fuel_prices, 'fuel', 'month')
t.calculate_foreign_key(df_trajectories, df_economy_indicators, 'economy_indicator', 'year')

print(df_trajectories.info())
print((df_trajectories.sample()))
