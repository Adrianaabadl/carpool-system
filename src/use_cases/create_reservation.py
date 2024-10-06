from faker import Faker
import random
from typing import List
from entities.models import *

Faker.seed(0)

class ReservationMocker:
    def __init__(self, trip_ids: List[int], passenger_ids: List[int]) -> None:
        self._faker = Faker()
        self.trip_ids = trip_ids
        self.passenger_ids = passenger_ids

    def generate_reservation(self) -> Reservation:
        trip_id = random.choice(self.trip_ids)
        passenger_id = random.choice(self.passenger_ids)
        reservation_date_time = self._faker.date_time_this_year()
        price_paid = round(random.uniform(10, 200), 2)

        return Reservation(
            trip_id=trip_id,
            passenger_id=passenger_id,
            reservation_date_time=reservation_date_time,
            price_paid=price_paid
        )

    def create_insert_query(self):
        insert_query = """
        INSERT INTO public.reservation (trip_id, passenger_id, reservation_date_time, price_paid)
        VALUES (%s, %s, %s, %s);
        """
        return insert_query
