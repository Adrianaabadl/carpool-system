SELECT
    COUNT(trip_id) as trips_count,
    SUM(total_distance_km) total_km
FROM `develop-431503.carpool_engine.dim_trip`
WHERE departure_date_time >= TIMESTAMP(DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), MONTH))
  AND departure_date_time < TIMESTAMP(DATE_TRUNC(CURRENT_DATE(), MONTH))
