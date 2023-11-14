WITH ClusteredPoints AS (
    SELECT
        t.id AS trajectory_id,
        (ST_DumpPoints(trajectory(t.route)::geometry)).geom AS point_geom
    FROM
        trajectory t
), ClusteredTrajectories AS (
    SELECT
        trajectory_id,
        ST_ClusterDBSCAN(point_geom, eps := 10, minpoints := 5) OVER () AS cluster_id
    FROM
        ClusteredPoints
), RankedClusters AS (
    SELECT
        ct.trajectory_id,
        ct.cluster_id,
        COUNT(*) AS point_count,
        ROW_NUMBER() OVER (PARTITION BY ct.trajectory_id ORDER BY COUNT(*) DESC) AS rank
    FROM
        ClusteredTrajectories ct
    GROUP BY
        ct.trajectory_id, ct.cluster_id
)

SELECT
    rc.trajectory_id,
    rc.cluster_id,
    ST_AsText(ST_ConvexHull(ST_Collect(cp.point_geom))) AS cluster_geometry
FROM
    RankedClusters rc
JOIN
    ClusteredPoints cp ON rc.trajectory_id = cp.trajectory_id
WHERE
    rc.rank = 1
GROUP BY
    rc.trajectory_id, rc.cluster_id
ORDER BY
    rc.cluster_id, rc.trajectory_id;
