SELECT
    b.hour,
    r.code_region,
    COUNT(t.id) AS num_trajectories,
    AVG(t.speed_average) AS avg_speed
FROM
    trajectory t
JOIN
    hour b ON t.date_id = b.id
JOIN
    region r ON t.region_id = r.id
GROUP BY
    b.hour, r.code_region
ORDER BY
    b.hour, r.code_region;
