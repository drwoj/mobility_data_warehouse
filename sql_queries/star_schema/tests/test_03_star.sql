SELECT
    t.country,
    AVG(t.distance) AS avg_distance,
    AVG(t.speed_average) AS avg_speed
FROM
    trajectory t
GROUP BY
    country
HAVING
    COUNT(t.id) > 10
ORDER BY
    avg_distance DESC
LIMIT 10; -- Adjust the limit based on your preference
