SELECT
    d.hour,
    r.code_region,
    COUNT(t.id) AS num_trajectories,
    AVG(t.speed_average) AS avg_speed
FROM
    trajectory t
JOIN
    date d ON t.date_id = d.id
JOIN
    region r ON t.region_id = r.id
GROUP BY
    d.hour, r.code_region
ORDER BY
    d.hour, r.code_region;
