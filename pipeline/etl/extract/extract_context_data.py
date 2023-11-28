import pandas as pd


def extract_weather(path_csv):
    df = pd.read_csv(path_csv,
                     skiprows=1,
                     header=None,
                     usecols=[1, 2, 3, 4, 5],
                     names=['timestamp', 'rain', 'temp_avg', 'temp_max', 'temp_min'])
    return df


path_weather_hannover = r'C:\Users\drwoj\Desktop\inzynierka\datasets\weather_hannover.csv'
path_weather_beijing = r'C:\Users\drwoj\Desktop\inzynierka\datasets\weather_beijing.csv'

df_weather_hannover = extract_weather(path_weather_hannover)
df_weather_beijing = extract_weather(path_weather_beijing)
