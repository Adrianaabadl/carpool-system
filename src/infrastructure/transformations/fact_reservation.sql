SELECT 
    distinct r.*
FROM reservation r 
JOIN trip t on r.trip_id = t.trip_id 
WHERE t.status = 'completed' 