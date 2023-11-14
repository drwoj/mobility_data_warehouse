-- Inserting sample data into the object_type table
INSERT INTO object_type (name) VALUES
    ('Car'),
    ('Truck'),
    ('Bus');

-- Inserting sample data into the weather table
INSERT INTO weather (rain, snow, temperature_avg, temperature_min, temperature_max) 
SELECT 
    random(), 
    random(), 
    random(), 
    random(), 
    random()
FROM generate_series(1, 10);

-- Inserting sample data into the fuel table
INSERT INTO fuel (type_fuel, price_fuel) 
SELECT 
    'Petrol', 
    random() * 2.5
FROM generate_series(1, 10);

-- Inserting sample data into the region table
INSERT INTO region (code_region, area) VALUES
    ('Region1', ST_GeographyFromText('POINT(0 0)')),
    ('Region2', ST_GeographyFromText('POINT(1 1)')),
    ('Region3', ST_GeographyFromText('POINT(2 2)'));

-- Inserting sample data into the economy_indicator table
INSERT INTO economy_indicator (
    population_total, population_male, population_female, 
    population_density, population_urban, population_urban_growth, 
    population_rural, population_rural_growth, population_largest_city, 
    population_ages_0_14, population_ages_15_64, population_ages_65_above, 
    mortality_road_traffic, co2_emissions_transport, 
    pm2_5_air_pollution, c02_emissions_gaseous_fuel, 
    rail_lines_total_length, railways_passengers_carried, 
    gdp_per_capita_constant, gdp_per_capita_current, 
    inflation_consumer_prices, unemployment_national_estimate, 
    uneployment_ilo_estimate, investment_in_transport
)
SELECT 
    random()*1000000000, random()*500000000, random()*500000000, 
    random()*500, random()*100000000, random(), 
    random()*1000000000, random(), random()*10000000, 
    random()*100000000, random()*500000000, 
    random()*500000000, random()*500000000, 
    random()*100, random()*100, 
    random()*100, random()*100, 
    random()*100, random()*1000000, 
    random()*1000000, random()*1000000, 
    random()*1000000, random()*1000000, 
    random()*1000000 
FROM generate_series(1, 10);
