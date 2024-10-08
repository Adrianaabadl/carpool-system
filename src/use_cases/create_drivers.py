from faker import Faker
import random
import uuid
from typing import List
from entities.models import *

cancellation_records = ['Rarely Cancels', 'Usually Cancels', 'Never Cancels']

class DriverMocker:
    def __init__(self, country_code: str, country_name) -> None:
        self._faker = Faker(country_code)
        self._country = country_name
        self._random_suffix = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=5))

    def _generate_driver(self) -> Driver:
        driver_id = str(uuid.uuid4())
        name = self._faker.first_name()
        email = f"{self._faker.user_name()}{self._random_suffix}@{self._faker.free_email_domain()}"
        date_of_birth = self._faker.date_of_birth(minimum_age=18, maximum_age=75)
        phone = self._faker.phone_number()
        rating = round(random.uniform(0.00, 5.00), 2)
        is_id_verified = random.choice([True, False])
        cancellation_record = random.choice(cancellation_records)
        
        return Driver(
            driver_id=driver_id,
            name=name,
            email=email,
            date_of_birth=date_of_birth,
            phone=phone,
            rating=rating,
            is_id_verified=is_id_verified,
            cancellation_record=cancellation_record
        )

    def _generate_drivers_list(self, num_drivers: int) -> List[Driver]:
        """Generates a list of Driver objects"""
        drivers = []
        for _ in range(num_drivers):
            driver = self._generate_driver()
            drivers.append(driver)
        return drivers

    def _create_insert_query(self, driver: Driver):
        """Generates the INSERT query using the values from the Driver object"""
        insert_query = """
        INSERT INTO public.driver (driver_id, name, email, date_of_birth, phone, rating, is_id_verified, cancellation_record)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            driver.driver_id,
            driver.name, 
            driver.email,
            driver.date_of_birth,
            driver.phone,
            driver.rating,
            driver.is_id_verified,
            driver.cancellation_record
        )
        return insert_query, values
