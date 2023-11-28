import pandas as pd


def extract_weather(path_csv):
    df = pd.read_csv(path_csv,
                     header=1,
                     usecols=[1, 2, 3, 4, 5],
                     names=['date', 'rain', 'temp_avg', 'temp_max', 'temp_min'])
    return df


def extract_fuel_from_sheet(path_excel, sheet_name, fuel_type):
    df = pd.read_excel(path_excel,
                       sheet_name=sheet_name,
                       header=None,
                       skiprows=19,
                       nrows=3,
                       usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    df = df.melt(id_vars=0, var_name='month', value_name=fuel_type)
    df[0] = df[0].str[:4]
    df['date'] = pd.to_datetime(df[0] + '-' + df['month'].astype(str) + '-01')
    df = df[['date', fuel_type]].sort_values(by='date').reset_index(drop=True)

    return df


def extract_fuel_hannover(path_excel):
    df_gasoline = extract_fuel_from_sheet(path_excel, '5.4.2 Petrol - €', 'gasoline')
    df_diesel = extract_fuel_from_sheet(path_excel, '5.5.2 Diesel fuel - €', 'diesel')
    df_combined = pd.merge(df_gasoline, df_diesel, on='date', how='outer')

    return df_combined


path_weather_hannover = r'C:\Users\drwoj\Desktop\inzynierka\datasets\weather_hannover.csv'
path_weather_beijing = r'C:\Users\drwoj\Desktop\inzynierka\datasets\weather_beijing.csv'
path_regions = r'C:\Users\drwoj\Desktop\inzynierka\datasets\regions.xlsx'
path_fuel_hannover = r'C:\Users\drwoj\Desktop\inzynierka\datasets\fuel_prices_hannover.xlsx'
path_fuel_beijing = r'C:\Users\drwoj\Desktop\inzynierka\datasets\fuel_prices_china.xlsx'

df_weather_hannover = extract_weather(path_weather_hannover)
df_weather_beijing = extract_weather(path_weather_beijing)
df_districts_hannover = pd.read_excel(path_regions, sheet_name='hannover')
df_districts_beijing = pd.read_excel(path_regions, sheet_name='beijing')
df_fuel_prices_hannover = extract_fuel_hannover(path_fuel_hannover)
df_fuel_prices_beijing = pd.read_excel(path_fuel_beijing, header=1,
                                       names=['date', 'gasoline', 'diesel'])

print(df_fuel_prices_beijing)
print(df_fuel_prices_hannover)
