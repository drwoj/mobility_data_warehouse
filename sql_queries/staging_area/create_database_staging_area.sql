CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS mobilitydb;

CREATE TABLE IF NOT EXISTS point (
    id SERIAL PRIMARY KEY,
    trajectory_id BIGINT,
    country VARCHAR(255),
    timestamp TIMESTAMP,
    coordinates GEOMETRY(POINT, 4326)
);
