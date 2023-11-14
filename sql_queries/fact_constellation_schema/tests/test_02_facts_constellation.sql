SELECT t.*, w.rain, w.snow, w.temperature_avg
FROM trajectory t
JOIN weather w ON t.weather_station_id = w.weather_station_id
JOIN country c ON t.country_id = c.id
WHERE c.name = 'Country1';
