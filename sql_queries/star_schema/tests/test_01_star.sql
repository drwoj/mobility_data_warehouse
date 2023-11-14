SELECT 
    t.country AS country_name,
    d.year AS data_year,
    d.month_name,
    d.day_name,
    ot.name AS object_type,
    r.code_region,
    ei.population_total,
    ei.gdp_per_capita_current,
    COUNT(t.id) AS num_trajectories,
    AVG(t.distance) AS avg_distance,
    MAX(w.temperature_max) AS max_temperature
FROM 
    trajectory t
JOIN 
    date d ON t.date_id = d.id
JOIN 
    object_type ot ON t.object_type_id = ot.id
JOIN 
    region r ON t.region_id = r.id
JOIN 
    economy_indicator ei ON t.economy_indicator_id = ei.id
JOIN 
    weather w ON t.weather_id = w.id
GROUP BY 
    t.country, d.year, d.month_name, d.day_name, ot.name, r.code_region, ei.population_total, ei.gdp_per_capita_current
ORDER BY 
    num_trajectories DESC;
