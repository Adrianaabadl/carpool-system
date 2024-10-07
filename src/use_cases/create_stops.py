from faker import Faker
from typing import List, Tuple
import random
import uuid
from entities.models import *
from use_cases.create_cities import CityMocker


class StopMocker:
    def __init__(self, country_code: str, country_name: str, trip_id, stop_order, previous_stop_id) -> None:
        self._country_code = country_code,
        self._country = country_name
        self._trip_id = trip_id
        self._stop_order = stop_order
        self._previous_stop_id = previous_stop_id
        self._faker = Faker(country_code)
        

    def _generate_stop(self) -> Stop:
        city_objet = self._generate_city(self._country_code, self._country)
        stop_id = str(uuid.uuid4())
        trip_id = self._trip_id
        city_id = city_objet.zip_code
        stop_order = self._stop_order
        price = round(random.uniform(5, 50), 2)
        distance_km = round(random.uniform(1, 200), 2)
        estimated_arrival_time = self._faker.date_time_this_year()
        previous_stop_id = self._previous_stop_id

        return Stop(
            stop_id=stop_id,
            trip_id=trip_id,
            city_id=city_id,
            stop_order=stop_order,
            price=price,
            distance_km=distance_km,
            estimated_arrival_time=estimated_arrival_time,
            previous_stop_id=previous_stop_id
        ), city_objet
    
    def _generate_city(self, country_code, country_name) -> City:
        city_mocker = CityMocker(country_code, country_name)
        city = city_mocker._generate_cities()[0]
        return city

    def _create_insert_query(self, city: City, stop: Stop ) -> List[Tuple[str, Tuple]]:
        insert_queries = []
        
        insert_query = """
        INSERT INTO public.city (city_name, zip_code, country)
        VALUES (%s, %s, %s)
        ON CONFLICT (city_name, zip_code) DO NOTHING;
        """
        values = (city.city_name, city.zip_code, city.country)
        insert_queries.append((insert_query, values))

        insert_query = """
        INSERT INTO public.stop (stop_id, trip_id, city_zip_code, stop_order, price, distance_km, estimated_arrival_time, previous_stop_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            stop.stop_id,
            stop.trip_id,
            stop.city_id,
            stop.stop_order,
            stop.price,
            stop.distance_km,
            stop.estimated_arrival_time,
            stop.previous_stop_id,
        )
        insert_queries.append((insert_query, values))
        
        return insert_queries