SELECT 
    DATE_TRUNC(DATE(departure_date_time), MONTH) AS date,
    destination_country as country,
    COUNT(trip_id) AS trips
FROM `develop-431503.carpool_engine.dim_trip`
GROUP BY date, destination_country
ORDER BY date DESC, destination_country