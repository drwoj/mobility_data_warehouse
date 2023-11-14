ALTER TABLE weather
ADD CONSTRAINT chk_weather_rain
CHECK (rain >= 0 AND rain <= 200),
ADD CONSTRAINT chk_weather_snow
CHECK (snow >= 0 AND snow <= 2000),
ADD CONSTRAINT chk_weather_temperature_avg
CHECK (temperature_avg >= -100 AND temperature_avg <= 100),
ADD CONSTRAINT chk_weather_temperature_min
CHECK (temperature_min >= -100 AND temperature_min <= 100),
ADD CONSTRAINT chk_weather_temperature_max
CHECK (temperature_max >= -100 AND temperature_max <= 100);

ALTER TABLE date
ADD CONSTRAINT chk_date_hour
CHECK (hour >= 0 AND hour < 24),
ADD CONSTRAINT chk_date_day
CHECK (day >= 1 AND day <= 31),
ADD CONSTRAINT chk_date_month
CHECK (month >= 1 AND month <= 12),
ADD CONSTRAINT chk_date_year
CHECK (year >= 2000 AND year <= 3000);

ALTER TABLE fuel
ADD CONSTRAINT chk_fuel_price
CHECK (price_fuel >= 0);

ALTER TABLE trajectory
ADD CONSTRAINT chk_trajectory_duration
CHECK (duration >= INTERVAL '0 seconds');

