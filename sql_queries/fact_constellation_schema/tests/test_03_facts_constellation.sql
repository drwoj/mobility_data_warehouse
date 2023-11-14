SELECT
    c.name AS country_name,
    AVG(t.distance) AS avg_distance,
    AVG(t.speed_average) AS avg_speed
FROM
    trajectory t
JOIN
    country c ON t.country_id = c.id
GROUP BY
    c.name
HAVING
    COUNT(t.id) > 10
ORDER BY
    avg_distance DESC
LIMIT 10; -- Adjust the limit based on your preference
