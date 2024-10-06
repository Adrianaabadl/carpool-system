from faker import Faker
import random
from typing import List
from entities.models import *

Faker.seed(0)

class PassengerMocker:
    def __init__(self, country_code: str, country_name) -> None:
        self._faker = Faker(country_code)
        self._country = country_name

    def generate_passenger(self) -> Passenger:
        name = self._faker.name()
        email = self._faker.email()
        phone = self._faker.phone_number()
        rating = round(random.uniform(0.00, 5.00), 2)

        return Passenger(
            name=name,
            email=email,
            phone=phone,
            rating=rating
        )

    def create_insert_query(self):
        insert_query = """
        INSERT INTO public.passenger (name, email, phone, rating)
        VALUES (%s, %s, %s, %s);
        """
        return insert_query
