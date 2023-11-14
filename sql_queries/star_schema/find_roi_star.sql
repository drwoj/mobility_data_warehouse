WITH IntersectingTrajectories AS (
    SELECT
        t1.id AS trajectory_id1,
        t2.id AS trajectory_id2,
        ST_Intersection(trajectory(t1.route)::geography,
						trajectory(t2.route)::geography) AS intersection_geom
    FROM
        trajectory t1
    JOIN
        trajectory t2 ON t1.id <> t2.id
    WHERE
        ST_Intersects(trajectory(t1.route), trajectory(t2.route))
)

SELECT
    ST_AsText(ST_ConvexHull(ST_Collect(intersection_geom::geometry))) AS region_of_interest
FROM
    IntersectingTrajectories
GROUP BY
    trajectory_id1
HAVING
    COUNT(*) >= 90;
