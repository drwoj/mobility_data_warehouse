select 
	id,
	startTimestamp(route) AS date,
	country,
	route,
	length(route)/1000 AS distance,
	duration(route) AS duration,
	twAvg(speed(route)) * 3.6 AS avg_speed
	
FROM trajectory