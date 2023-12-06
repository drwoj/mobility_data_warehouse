insert_date = """
INSERT INTO date (timestamp, year, month, day, hour, day_name, month_name)
SELECT 
    timestamp,
    EXTRACT(YEAR FROM timestamp) as year,
    EXTRACT(MONTH FROM timestamp) as month,
    EXTRACT(DAY FROM timestamp) as day,
    EXTRACT(HOUR FROM timestamp) as hour,
    TO_CHAR(timestamp, 'FMDay') as day_name,
    TO_CHAR(timestamp, 'FMMonth') as month_name
FROM generate_series(
    '2007-04-01 00:00:00'::TIMESTAMP, 
    '2012-08-31 23:59:59'::TIMESTAMP, 
    interval '1 hour'
) as timestamp
UNION ALL

SELECT 
    timestamp,
    EXTRACT(YEAR FROM timestamp) as year,
    EXTRACT(MONTH FROM timestamp) as month,
    EXTRACT(DAY FROM timestamp) as day,
    EXTRACT(HOUR FROM timestamp) as hour,
    TO_CHAR(timestamp, 'FMDay') as day_name,
    TO_CHAR(timestamp, 'FMMonth') as month_name
FROM generate_series(
    '2017-02-17 00:00:00'::TIMESTAMP, 
    '2019-03-27 23:59:59'::TIMESTAMP, 
    interval '1 hour'
) as timestamp;
"""

create_trajectories_from_points = """
SELECT 
	id,
	district_id,
	startTimestamp(route)::timestamp AS date,
	country,
	AsText(route) as route,
	length(route)/1000 AS distance,
	duration(route) AS duration,
	twAvg(speed(route)) * 3.6 AS avg_speed,
	ST_AsText(trajectory(route)) AS route_line
FROM trajectory
WHERE length(route) > 0 
AND duration(route) > '1 minute' 
AND twAvg(speed(route)) * 3.6 < 300
"""

select_districts = """
SELECT 
id, 
city, 
name, ST_AsText(area) AS area 
FROM district
"""

select_dates = 'SELECT id, timestamp::timestamp as date FROM date;'

create_mobility_dw = """
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS mobilitydb;

CREATE TABLE IF NOT EXISTS date (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_name VARCHAR(255),
    month_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    rain FLOAT,
	temperature_avg FLOAT,
	temperature_max FLOAT,
	temperature_min FLOAT
);

CREATE TABLE IF NOT EXISTS economy_indicator (
    id SERIAL PRIMARY KEY,
    population_total INTEGER,
	population_density FLOAT,
	population_urban INTEGER,
	population_urban_growth FLOAT,
	population_largest_city INTEGER,
	mortality_road_traffic FLOAT,
	co2_emissions_transport FLOAT,
	gdp_per_capita_constant FLOAT,
	gdp_per_capita_current FLOAT,
	inflation_consumer_prices FLOAT
);

CREATE TABLE IF NOT EXISTS fuel_price (
    id SERIAL PRIMARY KEY,
    gasoline FLOAT,
    diesel FLOAT
);

CREATE TABLE IF NOT EXISTS district (
    id SERIAL PRIMARY KEY,
	city VARCHAR(255),
    name VARCHAR(255),
	area GEOMETRY (MULTIPOLYGON, 4326)
);

CREATE TABLE IF NOT EXISTS trajectory (
    id SERIAL PRIMARY KEY,
    date_id INTEGER REFERENCES date(id),
    weather_id INTEGER REFERENCES weather(id),
	district_id INTEGER REFERENCES district(id),
    economy_indicator_id INTEGER REFERENCES economy_indicator(id),
    fuel_price_id INTEGER REFERENCES fuel_price(id),
    route TGEOGPOINT,
	distance FLOAT,
	duration INTERVAL,
    avg_speed FLOAT
);
"""

drop_mobility_db = """DROP TABLE IF EXISTS 
date, district, economy_indicator, fuel_price, trajectory, weather CASCADE
"""
