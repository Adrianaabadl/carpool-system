-- Create the fact table for reservations with partitioning and clustering
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.fact_reservation`
(
    reservation_id STRING NOT NULL OPTIONS(description="Unique identifier for the reservation."),
    trip_id STRING NOT NULL OPTIONS(description="ID of the trip associated with the reservation."),
    passenger_id STRING NOT NULL OPTIONS(description="ID of the passenger making the reservation."),
    reservation_date_time TIMESTAMP NOT NULL OPTIONS(description="Date and time of the reservation."),
    price_paid FLOAT64 NOT NULL OPTIONS(description="Total price paid for the reservation."),
    description STRING OPTIONS(description="Additional description for the reservation.")
)
PARTITION BY DATE(reservation_date_time)  -- Partitioning by reservation date
CLUSTER BY trip_id, passenger_id  -- Clustering by trip_id and passenger_id
OPTIONS(description="Fact table containing reservation details. This table is derived from `dim_trip`, `dim_passenger`, and source data from `reservations` in PostgreSQL.");

-- Create dimension table for passengers
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.dim_passenger`
(
    passenger_id STRING NOT NULL OPTIONS(description="Unique identifier for the passenger."),
    name STRING NOT NULL OPTIONS(description="Name of the passenger."),
    email STRING NOT NULL OPTIONS(description="Email address of the passenger."),
    description STRING OPTIONS(description="Additional description for the passenger.")
)
CLUSTER BY passenger_id 
OPTIONS(description="Dimension table for passenger details. This table is sourced from the `passengers` table in PostgreSQL.");

-- Create dimension table for trips
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.dim_trip`
(
    trip_id STRING NOT NULL OPTIONS(description="Unique identifier for the trip."),
    driver_id STRING NOT NULL OPTIONS(description="ID of the driver associated with the trip."),
    departure_city_id STRING NOT NULL OPTIONS(description="ID of the departure city."),
    destination_city_id STRING NOT NULL OPTIONS(description="ID of the destination city."),
    departure_date_time TIMESTAMP NOT NULL OPTIONS(description="Date and time of trip departure."),
    description STRING OPTIONS(description="Additional description for the trip.")
)
PARTITION BY DATE(departure_date_time)
CLUSTER BY trip_id, driver_id
OPTIONS(description="Dimension table for trip details. This table is sourced from the `trips` table in PostgreSQL.");

-- Create dimension table for drivers
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.dim_driver`
(
    driver_id STRING NOT NULL OPTIONS(description="Unique identifier for the driver."),
    name STRING NOT NULL OPTIONS(description="Name of the driver."),
    rating FLOAT64 OPTIONS(description="Driver's rating."),
    description STRING OPTIONS(description="Additional description for the driver.")
)
CLUSTER BY driver_id
OPTIONS(description="Dimension table for driver details. This table is sourced from the `drivers` table in PostgreSQL.");

-- Create dimension table for cities
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.dim_city`
(
    city_id INT64 NOT NULL OPTIONS(description="Unique identifier for the city."),
    city_name STRING NOT NULL OPTIONS(description="Name of the city."),
    zip_code STRING NOT NULL OPTIONS(description="Zip code of the city."),
    description STRING OPTIONS(description="Additional description for the city.")
)
CLUSTER BY city_id
OPTIONS(description="Dimension table for city details. This table is sourced from the `cities` table in PostgreSQL.");
