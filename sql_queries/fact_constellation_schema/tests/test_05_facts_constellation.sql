SELECT
    r.code_region AS region,
    e.gdp_per_capita_current AS gdp_per_capita,
    w.temperature_avg AS avg_temperature,
    COUNT(t.id) AS num_trajectories,
    AVG(t.speed_average) AS avg_speed
FROM
    trajectory t
JOIN
    region r ON t.region_id = r.id
JOIN
    economy_indicator e ON t.economy_indicator_id = e.id
JOIN
    weather w ON t.weather_station_id = w.weather_station_id
GROUP BY
    r.code_region, e.gdp_per_capita_current, w.temperature_avg
ORDER BY
    r.code_region, e.gdp_per_capita_current, w.temperature_avg;
