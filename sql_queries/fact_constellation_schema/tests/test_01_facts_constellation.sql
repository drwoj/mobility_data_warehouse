SELECT 
    c.name AS country_name,
    y.year AS data_year,
    m.month_name,
    d.day_name,
    o.name,
    r.code_region,
    e.population_total,
    e.gdp_per_capita_current,
    COUNT(t.id) AS num_trajectories,
    AVG(t.distance) AS avg_distance,
    MAX(w.temperature_max) AS max_temperature
FROM 
    trajectory t
JOIN 
    country c ON t.country_id = c.id
JOIN 
    hour b ON t.date_id = b.id
JOIN 
    day d ON d.id = b.day_id
JOIN 
    month m ON m.id = d.month_id
JOIN
    year y ON m.year_id = y.id
JOIN 
    object_type o ON t.object_type_id = o.id
JOIN 
    region r ON t.region_id = r.id
JOIN 
    economy_indicator e ON c.id = e.country_id AND y.id = e.year_id
JOIN 
    weather_station ws ON t.weather_station_id = ws.id
JOIN 
    weather w ON ws.id = w.weather_station_id AND b.day_id = d.id
GROUP BY 
    c.name, y.year, m.month_name, d.day_name, o.name, r.code_region, e.population_total, e.gdp_per_capita_current
HAVING 
    COUNT(t.id) > 10
ORDER BY 
    num_trajectories DESC;
