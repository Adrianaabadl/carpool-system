-- Create the fact table for reservations with partitioning and clustering
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.fact_reservation`
(
    reservation_id STRING NOT NULL OPTIONS(description="Unique identifier for the reservation."),
    trip_id STRING NOT NULL OPTIONS(description="ID of the trip associated with the reservation."),
    passenger_id STRING NOT NULL OPTIONS(description="ID of the passenger making the reservation."),
    reservation_date_time TIMESTAMP NOT NULL OPTIONS(description="Date and time of the reservation."),
    price_paid FLOAT64 NOT NULL OPTIONS(description="Total price paid for the reservation.")
)
PARTITION BY DATE(reservation_date_time)  -- Partitioning by reservation date
CLUSTER BY trip_id, passenger_id  -- Clustering by trip_id and passenger_id
OPTIONS(description="Fact table containing reservation details. This table is derived from `dim_trip`, `dim_passenger`, and source data from `reservations` in PostgreSQL.");

-- Create dimension table for passengers
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.dim_passenger`
(
    passenger_id STRING NOT NULL OPTIONS(description="Unique identifier for the passenger."),
    name STRING NOT NULL OPTIONS(description="Name of the passenger."),
    rating FLOAT64 NOT NULL OPTIONS(description="Passengers rating.")
    
)
CLUSTER BY passenger_id 
OPTIONS(description="Dimension table for passenger details. This table is sourced from the `passengers` table in PostgreSQL.");

-- Create dimension table for trips
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.dim_trip`
(
    trip_id STRING NOT NULL OPTIONS(description="Unique identifier for the trip."),
    driver_id STRING NOT NULL OPTIONS(description="ID of the driver associated with the trip."),
    departure_city STRING NOT NULL OPTIONS(description="Name of the departure city."),
    destination_city STRING NOT NULL OPTIONS(description="Name of the destination city."),
    destination_country STRING OPTIONS(description="Country of the destination city."),
    departure_date_time TIMESTAMP NOT NULL OPTIONS(description="Date and time of trip departure."),
    number_of_stops INT64 NOT NULL OPTIONS(description="Number of stops in the trip."),
    number_of_seats INT64 NOT NULL OPTIONS(description="Number of seats available for the trip."),
    total_distance_km FLOAT64 NOT NULL OPTIONS(description="Total distance of the trip in kilometers.")
)
PARTITION BY DATE(departure_date_time)
CLUSTER BY trip_id, driver_id
OPTIONS(description="Dimension table for trip details. This table is sourced from the `trips` table in PostgreSQL and joined with city data.");

-- Create dimension table for drivers
CREATE TABLE IF NOT EXISTS `develop-431503.carpool_engine.dim_driver`
(
    driver_id STRING NOT NULL OPTIONS(description="Unique identifier for the driver."),
    name STRING NOT NULL OPTIONS(description="Name of the driver."),
    is_id_verified BOOLEAN OPTIONS(description="Indicates if the driver's ID is verified."),
    rating FLOAT64 OPTIONS(description="Driver's rating."),
    total_rides_published INT64 OPTIONS(description="Total rides published by the driver."),
    member_since DATE OPTIONS(description="Date when the driver became a member.")
)
CLUSTER BY driver_id
OPTIONS(description="Dimension table for driver details. This table is sourced from the `drivers` and `driver_preferences` tables in PostgreSQL.");