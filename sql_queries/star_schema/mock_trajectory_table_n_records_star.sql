INSERT INTO trajectory (
    object_type_id, economy_indicator_id, region_id, date_id, weather_id, fuel_id,
    route, distance, duration, speed_average, country
)
SELECT 
    floor(random() * (SELECT COUNT(*) FROM object_type) + 1) object_type_id,
    floor(random() * (SELECT COUNT(*) FROM economy_indicator) + 1) economy_indicator_id,
    floor(random() * (SELECT COUNT(*) FROM region) + 1) as region_id,
    floor(random() * (SELECT COUNT(*) FROM date) + 1) as date_id,
    floor(random() * (SELECT COUNT(*) FROM weather) + 1) as weather_id,
    floor(random() * (SELECT COUNT(*) FROM fuel) + 1) as fuel_id,
    TGeogPoint(
        '{[' || 
            'Point(' || 
            (floor(random() * 360 - 180)) || ' ' || 
            (floor(random() * 180 - 90)) || 
            ')@2001-01-01 08:10:00,' ||
		 'Point(' || 
            (floor(random() * 360 - 180)) || ' ' || 
            (floor(random() * 180 - 90)) || 
            ')@2001-01-01 08:10:01,' ||
		 'Point(' || 
            (floor(random() * 360 - 180)) || ' ' || 
            (floor(random() * 180 - 90)) || 
            ')@2001-01-01 08:10:02,' ||
		 'Point(' || 
            (floor(random() * 360 - 180)) || ' ' || 
            (floor(random() * 180 - 90)) || 
            ')@2001-01-01 08:10:03,' ||
		 'Point(' || 
            (floor(random() * 360 - 180)) || ' ' || 
            (floor(random() * 180 - 90)) || 
            ')@2001-01-01 08:10:04'
         || ']}'
    ) as route,
    random() * 500 as distance,
    (floor(random() * 360)::text || ' minutes')::interval as duration,
    random() * 100 as speed_average,
    'Country' || floor(random() * 3) + 1 as country
FROM generate_series(1, 1000);

select * from trajectory