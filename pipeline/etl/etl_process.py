import pandas as pd

import etl.extract.extract_context_data as e
import paths as p


df_weather_hannover = e.extract_weather(p.path_weather_hannover)
df_weather_beijing = e.extract_weather(p.path_weather_beijing)
df_districts_hannover = e.pd.read_excel(p.path_regions, sheet_name='hannover')
df_districts_beijing = e.pd.read_excel(p.path_regions, sheet_name='beijing')
df_fuel_prices_hannover = e.extract_fuel_hannover(p.path_fuel_hannover)
df_fuel_prices_beijing = pd.read_excel(p.path_fuel_beijing,
                                       header=1,
                                       names=['date', 'gasoline', 'diesel'])
df_economy_indicators = e.extract_economy_indicators(p.path_economy)

df_weather_hannover['city'] = 'Hannover'
df_weather_beijing['city'] = 'Beijing'
df_districts_hannover['city'] = 'Hannover'
df_districts_beijing['city'] = 'Beijing'
df_fuel_prices_hannover['city'] = 'Hannover'
df_fuel_prices_beijing['city'] = 'Beijing'

df_weather = pd.concat([df_weather_beijing, df_weather_hannover], ignore_index=True)
df_districts = pd.concat([df_districts_beijing, df_districts_hannover], ignore_index=True)
df_fuel_prices = pd.concat([df_fuel_prices_beijing, df_fuel_prices_hannover], ignore_index=True)
df_trajectories = e.extract_trajectories()
