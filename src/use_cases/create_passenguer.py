from faker import Faker
import random
import uuid
from entities.models import *

Faker.seed(0)

class PassengerMocker:
    def __init__(self, country_code: str) -> None:
        self._faker = Faker(country_code)

    def _generate_passenger(self) -> Passenger:
        passenger_id = str(uuid.uuid4())
        name = self._faker.name()
        email = self._faker.email()
        phone = self._faker.phone_number()
        rating = round(random.uniform(0.00, 5.00), 2)

        return Passenger(
            passenger_id=passenger_id,
            name=name,
            email=email,
            phone=phone,
            rating=rating
        )

    # def _create_insert_query(self):
    #     insert_query = """
    #     INSERT INTO public.passenger (passenger_id, name, email, phone, rating)
    #     VALUES (%s,%s, %s, %s, %s);
    #     """
    #     return insert_query