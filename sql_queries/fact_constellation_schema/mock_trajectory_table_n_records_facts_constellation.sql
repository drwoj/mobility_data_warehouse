INSERT INTO trajectory (
    object_type_id, economy_indicator_id, weather_station_id, region_id, 
    date_id, country_id, route, distance, duration, speed_average
) 
SELECT 
    floor(random() * (SELECT COUNT(*) FROM object_type) + 1) as object_type_id, 
    floor(random() * (SELECT COUNT(*) FROM economy_indicator) + 1) as economy_indicator_id, 
    floor(random() * (SELECT COUNT(*) FROM weather_station) + 1) as weather_station_id, 
    floor(random() * (SELECT COUNT(*) FROM region) + 1) as region_id, 
    floor(random() * (SELECT COUNT(*) FROM hour) + 1) as date_id,
    floor(random() * (SELECT COUNT(*) FROM country) + 1) as country_id,
    TGeogPoint(
        '{[Point(0 0)@2001-01-01 08:00:00, Point(2 0)@2001-01-01 08:10:00, Point(2 1)@2001-01-01 08:15:00]}'::tgeompoint
    ) as route, 
    random()*500 as distance, 
    (floor(random()*360)::text || ' minutes')::interval as duration, 
    random()*100 as speed_average
FROM generate_series(1, 10000);
