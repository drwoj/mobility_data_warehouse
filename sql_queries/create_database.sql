CREATE TABLE IF NOT EXISTS object_Type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

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
    snow FLOAT,
	temperature_avg FLOAT,
	temperature_max FLOAT,
	temperature_min FLOAT
);

CREATE TABLE IF NOT EXISTS economy_indicator (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT
);

CREATE TABLE IF NOT EXISTS fuel (
    id SERIAL PRIMARY KEY,
    price FLOAT,
    type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS region (
    id SERIAL PRIMARY KEY,
    code_region VARCHAR(255),
	area GEOGRAPHY
);


CREATE TABLE IF NOT EXISTS trajectory (
    id SERIAL PRIMARY KEY,
    object_type_id INTEGER REFERENCES object_Type(id),
    begin_date_id INTEGER REFERENCES date(id),
	end_date_id INTEGER REFERENCES date(id),
    weather_id INTEGER REFERENCES weather(id),
    economy_indicator_id INTEGER REFERENCES economy_indicator(id),
    fuel_id INTEGER REFERENCES fuel(id),
    region_id INTEGER REFERENCES region(id),
    route TGEOGPOINT,
	distance FLOAT,
    avg_speed FLOAT,
    duration INTERVAL,
    country VARCHAR(255)
);
