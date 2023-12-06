CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS mobilitydb;

CREATE TABLE IF NOT EXISTS point (
    id SERIAL PRIMARY KEY,
    trajectory_id BIGINT,
    country VARCHAR(255),
    timestamp TIMESTAMP,
    coordinates GEOMETRY(POINT, 4326)
);

CREATE TABLE IF NOT EXISTS district (
    id SERIAL PRIMARY KEY,
	city VARCHAR(255),
    name VARCHAR(255),
	area GEOMETRY (MULTIPOLYGON, 4326)
);

CREATE TABLE IF NOT EXISTS trajectory (
	id SERIAL PRIMARY KEY,
	district_id  INTEGER,
	country VARCHAR(255),
	timestamp timestamp,
	route tgeogpoint
);

CREATE INDEX district_area_gist ON district USING GIST (area);
CREATE INDEX trajectory_route_gist ON trajectory USING GIST (route);