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
	startTimestamp(route)::timestamp AS date,
	country,
	AsText(route) as route,
	length(route)/1000 AS distance,
	duration(route) AS duration,
	twAvg(speed(route)) * 3.6 AS avg_speed,
	ST_AsText(ST_Centroid(trajectory(route))) AS center_point
FROM trajectory
"""

select_dates = 'SELECT id, timestamp::timestamp as date FROM date;'
