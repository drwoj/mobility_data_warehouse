CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS mobilitydb;

CREATE TABLE IF NOT EXISTS country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS year (
    id SERIAL PRIMARY KEY,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS month (
    id SERIAL PRIMARY KEY,
    year_id INTEGER REFERENCES year(id),
    month INTEGER,
    month_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS day (
    id SERIAL PRIMARY KEY,
    month_id INTEGER REFERENCES month(id),
    day INTEGER,
    day_name VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS hour (
    id SERIAL PRIMARY KEY,
    day_id INTEGER REFERENCES day(id),
    hour INTEGER
);

CREATE TABLE IF NOT EXISTS object_type (
    id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS region (
    id SERIAL PRIMARY KEY,
    code_region VARCHAR(255),
    area GEOGRAPHY NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS weather_station (
    id SERIAL PRIMARY KEY,
    point GEOGRAPHY NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    weather_station_id INTEGER REFERENCES weather_station(id),
    day_id INTEGER REFERENCES day(id),
    rain FLOAT,
    snow FLOAT,
    temperature_avg FLOAT,
    temperature_min FLOAT,
    temperature_max FLOAT
);

CREATE TABLE IF NOT EXISTS fuel (
    id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES country(id),
    month_id INTEGER REFERENCES month(id),
    type_fuel VARCHAR(255),
    price_fuel FLOAT
);

CREATE TABLE IF NOT EXISTS economy_indicator (
    id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES country(id),
    year_id INTEGER REFERENCES year(id),
    population_total INTEGER,
	population_male INTEGER,
	population_female INTEGER,
	population_density FLOAT,
	population_urban INTEGER,
	population_urban_growth FLOAT,
	population_rural INTEGER,
	population_rural_growth FLOAT,
	population_largest_city INTEGER,
	population_ages_0_14 INTEGER,
	population_ages_15_64 INTEGER,
	population_ages_65_above INTEGER,
	mortality_road_traffic FLOAT,
	co2_emissions_transport FLOAT,
	pm2_5_air_pollution FLOAT,
	c02_emissions_gaseous_fuel FLOAT,
	rail_lines_total_length FLOAT,
	railways_passengers_carried INTEGER,
	gdp_per_capita_constant FLOAT,
	gdp_per_capita_current FLOAT,
	inflation_consumer_prices FLOAT,
	unemployment_national_estimate FLOAT,
	uneployment_ilo_estimate FLOAT,
	investment_in_transport INTEGER
);

CREATE TABLE IF NOT EXISTS trajectory (
    id SERIAL PRIMARY KEY,
    object_type_id INTEGER REFERENCES object_type(id),
	economy_indicator_id INTEGER REFERENCES economy_indicator(id),
	region_id INTEGER REFERENCES region(id),
    date_id INTEGER REFERENCES hour(id),
	weather_station_id INTEGER REFERENCES weather_station(id),
    country_id INTEGER REFERENCES country(id),
    route TGEOGPOINT,
    distance FLOAT,
    duration INTERVAL,
    speed_average FLOAT
);
