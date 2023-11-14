INSERT INTO year (year) VALUES
    (2007),
    (2008),
    (2009),
    (2010),
    (2011),
    (2012),
    (2017),
    (2018),
    (2019);

INSERT INTO month (year_id, month, month_name)
SELECT 
    y.id, 
    s,
    CASE s
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END
FROM year y, generate_series(1, 12) as s;

INSERT INTO day (month_id, day, day_name)
SELECT 
    m.id,
    d,
    CASE 
        WHEN d <= CASE 
            WHEN m.month = 2 AND y.year IN (2008, 2012) THEN 29
            WHEN m.month = 2 THEN 28
            WHEN m.month IN (1, 3, 5, 7, 8, 10, 12) THEN 31
            ELSE 30
        END THEN
            TO_CHAR(date_trunc('month', (y.year || '-' || LPAD(m.month::text, 2, '0') || '-01')::date) + (d - 1) * INTERVAL '1 day', 'Day')
    END
FROM month m
JOIN year y ON m.year_id = y.id,
LATERAL generate_series(1, 
    CASE 
        WHEN m.month = 2 AND y.year IN (2008, 2012) THEN 29
        WHEN m.month = 2 THEN 28
        WHEN m.month IN (1, 3, 5, 7, 8, 10, 12) THEN 31
        ELSE 30
    END
) as d;

INSERT INTO hour (day_id, hour)
SELECT 
    d.id, 
    generate_series(0, 23)
FROM day d;
