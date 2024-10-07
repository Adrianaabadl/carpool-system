SELECT 
    t.trip_id,
    t.driver_id,
    dep.city_name AS departure_city,
    dest.city_name AS destination_city,
    dest.country AS destination_country,
    t.departure_date_time,
    t.number_of_stops,
    t.number_of_seats,
    t.total_distance_km 
FROM trip t
JOIN city dep ON t.departure_city_id = dep.zip_code
JOIN city dest ON t.destination_city_id = dest.zip_code
WHERE t.status = 'completed'