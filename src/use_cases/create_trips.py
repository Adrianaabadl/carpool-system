from faker import Faker
import random
from entities.models import *
import uuid


class TripMocker:
    def __init__(self, country_code: str,
                 departure_city_id,
                 destination_city_id,
                 driver_id ) -> None:

        self._faker = Faker(country_code)
        self._departure_city_id = departure_city_id
        self._destination_city_id = destination_city_id
        self._driver_id = driver_id

    def _generate_trip(self) -> Trip:
        departure_date_time = self._faker.date_time_this_year()
        number_of_stops = random.randint(0, 5)
        number_of_seats = random.randint(1, 4)
        price_per_seat = round(random.uniform(10, 100), 2)
        women_only = random.choice([True, False])
        enabled_instant_booking = random.choice([True, False])
        total_distance_km = round(random.uniform(50, 1000), 2)
        status = random.choice(['scheduled', 'ongoing', 'completed', 'cancelled'])
        additional_comments = self._faker.text(max_nb_chars=200)

        return Trip(
            trip_id = str(uuid.uuid4()),
            driver_id=self._driver_id,
            departure_city_id=self._departure_city_id,
            destination_city_id=self._destination_city_id,
            departure_date_time=departure_date_time,
            number_of_stops=number_of_stops,
            number_of_seats=number_of_seats,
            price_per_seat=price_per_seat,
            women_only=women_only,
            enabled_instant_booking=enabled_instant_booking,
            total_distance_km=total_distance_km,
            status=status,
            additional_comments=additional_comments
        )


    def _create_insert_query(self, trip: Trip):
        """Generate the insert query using the values of the Trip object."""
        insert_query = """
        INSERT INTO public.trip (trip_id, driver_id, departure_city_id, destination_city_id, departure_date_time, 
                                 number_of_stops, number_of_seats, price_per_seat, women_only, 
                                 enabled_instant_booking, total_distance_km, status, additional_comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            trip.trip_id,
            trip.driver_id,
            trip.departure_city_id,
            trip.destination_city_id,
            trip.departure_date_time,
            trip.number_of_stops,
            trip.number_of_seats,
            trip.price_per_seat,
            trip.women_only,
            trip.enabled_instant_booking,
            trip.total_distance_km,
            trip.status,
            trip.additional_comments
        )
        return insert_query, values
