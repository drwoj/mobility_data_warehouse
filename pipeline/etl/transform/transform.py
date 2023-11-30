import pandas as pd


def calculate_foreign_key(df_fact, df_dim, foreign_key, date_granularity='day'):
    granularity_formats = {
        'day': '%Y-%m-%d',
        'month': '%Y-%m',
        'year': '%Y'
    }

    format_string = granularity_formats.get(date_granularity, '%Y-%m-%d')
    df_fact['temp_date'] = pd.to_datetime(df_fact['date']).dt.strftime(format_string)
    df_dim['date'] = pd.to_datetime(df_dim['date']).dt.strftime(format_string)

    df_merged = pd.merge(df_fact, df_dim,
                         how='left',
                         left_on=['city', 'temp_date'],
                         right_on=['city', 'date'],
                         suffixes=('_trajectory', '_' + foreign_key))

    df_fact.drop(columns=['temp_date'], inplace=True)
    df_fact[foreign_key + '_id'] = df_merged['id_' + foreign_key]

    return df_fact


def country_to_city(df):
    df.loc[df['country'] == 'China', 'country'] = 'Beijing'
    df.loc[df['country'] == 'Germany', 'country'] = 'Hannover'

    df.rename(columns={'country': 'city'}, inplace=True)
    return df


def add_foreign_key_columns(df):
    df.insert(1, 'date_id', None)
    df.insert(2, 'district_id', None)
    df.insert(3, 'weather_id', None)
    df.insert(4, 'economy_indicator_id', None)
    df.insert(5, 'fuel_id', None)

    return df


def filter_weather_station(df, station):
    df = df[df['station'] == station]
    return df
