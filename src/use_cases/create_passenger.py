from faker import Faker
import random
import uuid
from entities.models import *

class PassengerMocker:
    def __init__(self, country_code: str) -> None:
        self._faker = Faker(country_code)
        self._random_suffix = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=5))

    def _generate_passenger(self) -> Passenger:
        passenger_id = str(uuid.uuid4())
        name = self._faker.name()
        email = f"{self._faker.user_name()}{self._random_suffix}@{self._faker.free_email_domain()}"
        phone = self._faker.phone_number()
        rating = round(random.uniform(0.00, 5.00), 2)

        return Passenger(
            passenger_id=passenger_id,
            name=name,
            email=email,
            phone=phone,
            rating=rating
        )