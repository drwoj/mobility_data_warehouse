-- Indexes for the trajectory table
CREATE INDEX idx_trajectory_object_type_id ON trajectory(object_type_id);
CREATE INDEX idx_trajectory_economy_indicator_id ON trajectory(economy_indicator_id);
CREATE INDEX idx_trajectory_region_id ON trajectory(region_id);
CREATE INDEX idx_trajectory_date_id ON trajectory(date_id);
CREATE INDEX idx_trajectory_weather_station_id ON trajectory(weather_station_id);
CREATE INDEX idx_trajectory_country_id ON trajectory(country_id);

-- Indexes for the economy_indicator table
CREATE INDEX idx_economy_indicator_country_year ON economy_indicator(country_id, year_id);

-- Indexes for the fuel table
CREATE INDEX idx_fuel_country_month ON fuel(country_id, month_id);

-- Indexes for the weather table
CREATE INDEX idx_weather_weather_station_day ON weather(weather_station_id, day_id);
CREATE INDEX idx_weather_station_temp_avg ON weather(weather_station_id, temperature_avg);
CREATE INDEX idx_weather_station_temp_avg ON weather(weather_station_id, snow);
CREATE INDEX idx_weather_station_temp_avg ON weather(weather_station_id, rain);

-- Indexes for the date hierarchical dimension table
CREATE INDEX idx_hour_day_id ON hour(day_id);
CREATE INDEX idx_day_month_id ON day(month_id);
CREATE INDEX idx_month_year_id ON month(year_id);
CREATE INDEX idx_year ON year(year);