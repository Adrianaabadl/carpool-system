from faker import Faker
import random
import uuid
from entities.models import *

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