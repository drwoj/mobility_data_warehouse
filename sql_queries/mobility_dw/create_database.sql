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
	inflation_consumer_prices FLOAT,
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
	area GEOGRAPHY
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
