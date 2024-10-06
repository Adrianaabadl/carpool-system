from faker import Faker
import random
from typing import List
from entities.models import *

Faker.seed(0)

class StopMocker:
    def __init__(self, trip_ids: List[int], city_ids: List[int]) -> None:
        self._faker = Faker()
        self.trip_ids = trip_ids
        self.city_ids = city_ids

    def generate_stop(self) -> Stop:
        trip_id = random.choice(self.trip_ids)
        city_id = random.choice(self.city_ids)
        stop_order = random.randint(1, 5)
        price = round(random.uniform(5, 50), 2)
        distance_km = round(random.uniform(1, 200), 2)
        estimated_arrival_time = self._faker.date_time_this_year()
        previous_stop_id = None  # Could be None or another stop ID

        return Stop(
            trip_id=trip_id,
            city_id=city_id,
            stop_order=stop_order,
            price=price,
            distance_km=distance_km,
            estimated_arrival_time=estimated_arrival_time,
            previous_stop_id=previous_stop_id
        )

    def create_insert_query(self):
        insert_query = """
        INSERT INTO public.stop (trip_id, city_id, stop_order, price, distance_km, estimated_arrival_time, previous_stop_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        return insert_query
