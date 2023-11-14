select * from trajectory t
JOIN weather w ON t.weather_id = w.id
WHERE t.country = 'Country1'