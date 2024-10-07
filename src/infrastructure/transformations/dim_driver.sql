SELECT 
    d.driver_id, 
    d.name, 
    d.is_id_verified, 
    d.rating, 
    dp.total_rides_published, 
    dp.member_since 
FROM public.driver d
LEFT JOIN public.driver_preferences dp ON dp.driver_id = d.driver_id