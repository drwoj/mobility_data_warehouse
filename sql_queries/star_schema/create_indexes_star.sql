-- Indexes for the trajectory table
CREATE INDEX idx_trajectory_object_type_id ON trajectory(object_type_id);
CREATE INDEX idx_trajectory_economy_indicator_id ON trajectory(economy_indicator_id);
CREATE INDEX idx_trajectory_region_id ON trajectory(region_id);
CREATE INDEX idx_trajectory_date_id ON trajectory(date_id);
CREATE INDEX idx_trajectory_weather_id ON trajectory(weather_id);

-- Indexes for the date table
CREATE INDEX idx_date_timestamp ON date (timestamp);
CREATE INDEX idx_date_year ON date (year);
CREATE INDEX idx_date_month ON date (month);
CREATE INDEX idx_date_day ON date (day);

-- Indexes for the weather talbe
CREATE INDEX idx_weather_snow ON weather (snow);
CREATE INDEX idx_weather_rain ON weather (rain);
CREATE INDEX idx_weather_temperature_avg ON weather (temperature_avg);

