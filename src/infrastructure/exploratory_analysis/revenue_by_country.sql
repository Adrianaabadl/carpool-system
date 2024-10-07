WITH target_data AS 
(SELECT 
    DATE(DATE_TRUNC(r.reservation_date_time,MONTH)) AS date,
    r.trip_id,
    t.destination_country as country,
    r.price_paid
FROM `develop-431503.carpool_engine.fact_reservation`  r   
JOIN `develop-431503.carpool_engine.dim_trip` t using (trip_id)  
)

SELECT
   date,
   country,
   sum(price_paid) earnings,
   count(trip_id) as trips
from target_data
GROUP BY 1,2 
ORDER BY 1 DESC