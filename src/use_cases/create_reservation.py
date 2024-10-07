from faker import Faker
import random
from entities.models import *
import uuid
from use_cases.create_passenger import PassengerMocker

Faker.seed(0)

class ReservationMocker:
    def __init__(self, country_code: str, country_name: str, trip_id) -> None:
        self._country_code = country_code
        self._country_name = country_name
        self._trip_id = trip_id
        self._faker = Faker(country_code)

    def _generate_reservation(self) -> Reservation:
        passenger_object = self._create_passenger(self._country_code)
        trip_id = self._trip_id
        reservation_date_time = self._faker.date_time_this_year()
        price_paid = round(random.uniform(10, 200), 2)

        return Reservation(
            reservation_id=str(uuid.uuid4()),
            trip_id=trip_id,
            reservation_date_time=reservation_date_time,
            passenger_id=passenger_object.passenger_id,
            price_paid=price_paid
        ), passenger_object

    def _create_passenger(self, country_code):
        passenguer_mocker = PassengerMocker(country_code)
        passenger = passenguer_mocker._generate_passenger()
        return passenger

    def _create_insert_query(self, passenger: Passenger, reservation: Reservation):
        insert_queries = []

        insert_query = """
        INSERT INTO public.passenger (passenger_id, name, email, phone, rating)
        VALUES (%s,%s, %s, %s, %s);
        """
        values = (passenger.passenger_id, passenger.name, passenger.email, passenger.phone, passenger.rating)
        insert_queries.append((insert_query, values))
        
        insert_query = """
        INSERT INTO public.reservation (reservation_id, trip_id, passenger_id, reservation_date_time, price_paid)
        VALUES (%s, %s, %s, %s, %s);
        """
        values = (reservation.reservation_id, reservation.trip_id, reservation.passenger_id, reservation.reservation_date_time, reservation.price_paid)
        insert_queries.append((insert_query, values))

        return insert_queries
