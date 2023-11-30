import pandas as pd

from database.connectors.StagingAreaConnector import StagingAreaConnector
from database.sql_queries import create_trajectories_from_points


def extract_weather(path_csv):
    df = pd.read_csv(path_csv,
                     header=1,
                     usecols=[0, 1, 2, 3, 4, 5],
                     names=['station', 'date', 'rain', 'temp_avg', 'temp_max', 'temp_min'])
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


def extract_economy_indicators(path_excel):
    df = pd.read_excel(path_excel,
                       sheet_name='Data',
                       header=0,
                       usecols=[0, 2, 4, 5, 6, 7, 8, 9, 10, 11],
                       nrows=25)

    df = df.melt(id_vars=['Country Name', 'Series Name', ],
                 var_name='year',
                 value_name='value')

    df = df.pivot_table(index=['year', 'Country Name'],
                        columns='Series Name',
                        values='value',
                        aggfunc='first').reset_index()

    df['year'] = df['year'].str[:4]
    df['year'] = df['year'].astype(int)

    df.columns.name = None
    df = df.rename(columns={'Country Name': 'country', 'year': 'date'})

    return df


def extract_trajectories():
    with StagingAreaConnector() as connector:
        df = connector.execute_select_query(create_trajectories_from_points)
        return df
