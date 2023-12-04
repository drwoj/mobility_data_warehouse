import pandas as pd


def calculate_foreign_key(df_fact, df_dim, foreign_key, date_granularity='day'):
    format_date_column(df_fact, date_granularity)
    format_date_column(df_dim, date_granularity)

    df_merged = pd.merge(df_fact, df_dim,
                         how='left',
                         on=['city', 'temp_date'],
                         suffixes=('_trajectory', '_' + foreign_key))

    df_fact.drop(columns=['temp_date'], inplace=True)
    df_dim.drop(columns=['temp_date'], inplace=True)

    df_fact[foreign_key + '_id'] = df_merged['id_' + foreign_key]


def format_date_column(df, date_granularity='day'):
    granularity_formats = {
        'day': '%Y-%m-%d',
        'month': '%Y-%m',
        'year': '%Y',
        'hour': '%Y-%m-%d %H'
    }
    format_string = granularity_formats.get(date_granularity, '%Y-%m-%d')
    df['temp_date'] = pd.to_datetime(df['date']).dt.strftime(format_string)


def extend_year_to_full_date(df):
    df['date'] = pd.to_datetime(df['date'].astype(str) + '-01-01')


def country_to_city(df):
    df.loc[df['country'] == 'China', 'country'] = 'Beijing'
    df.loc[df['country'] == 'Germany', 'country'] = 'Hannover'
    df.rename(columns={'country': 'city'}, inplace=True)


def convert_euros_per_hectolitre_to_euros_per_liter(df):
    df[['diesel', 'gasoline']] = df[['diesel', 'gasoline']].apply(lambda x: x / 100)


def convert_rmb_per_ton_to_euros_per_liter(df, conversion, weight):
    df[['diesel', 'gasoline']] = df[['diesel', 'gasoline']].apply(lambda x: x * conversion / weight)


def filter_weather_station(df, station):
    df = [df['station'] == station]


def is_point_in_region(point, district):
    return point.within(district)


def find_matching_regions(df_trajectories, df_regions):
    for _, trajectory in df_trajectories.iterrows():
        center_point = trajectory['center_point']
        trajectory_city = trajectory['city']

        matching_regions = df_regions[df_regions['city'] == trajectory_city]

        for _, region in matching_regions.iterrows():
            region_polygon = region['region_polygon']

            if is_point_in_region(center_point, region_polygon):
                df_trajectories.at[trajectory['id'], 'district_id'] = region['id']
                break


def calculate_date_id(df_trajectories, df_dates):
    format_date_column(df_trajectories, 'hour')
    format_date_column(df_dates, 'hour')

    df_merged = pd.merge(df_trajectories, df_dates,
                         how='left',
                         on='temp_date',
                         suffixes=('_trajectory', '_date'))

    df_trajectories.drop(columns=['temp_date'], inplace=True)
    df_dates.drop(columns=['temp_date'], inplace=True)

    df_trajectories['date_id'] = df_merged['id_date']
