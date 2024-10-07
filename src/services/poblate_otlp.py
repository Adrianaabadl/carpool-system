from infrastructure.database import DbManager
from use_cases.create_cities import CityMocker 
from use_cases.create_drivers import DriverMocker 
from use_cases.create_driver_preferences import DriverPreferencesMocker
from use_cases.create_trips import TripMocker
from use_cases.create_stops import StopMocker
from use_cases.create_reservation import ReservationMocker
import random

class PoblateDB:
    countries = {
        'France': 'fr_FR',
        'Spain': 'es_ES',
        'Germany': 'de_DE',
        'United Kingdom': 'en_GB',
        'Portugal': 'pt_PT',
        'Netherlands': 'nl_NL',
        'Italy': 'it_IT',
        'Mexico': 'es_MX',
        'Brazil': 'pt_BR'
    }

    def __init__(self, num_entries=10):
        self.num_entries = num_entries

    def run(self):
        db_manager = DbManager()
        db_manager._create_connection()
        try:
            for _ in range(self.num_entries):
                random_country = random.choice(list(self.countries.keys()))

                """Insert cities"""
                city_mocker = CityMocker(country_code=f"{self.countries[random_country]}", country_name=random_country)
                origin_city, destination_city = city_mocker._generate_cities()
                insert_queries = city_mocker._create_insert_query([origin_city,destination_city])
                for element in insert_queries:
                    insert_query, values = element
                    db_manager._execute_query(insert_query, values)

                """Insert driver"""
                driver_mocker = DriverMocker(country_code=f"{self.countries[random_country]}", country_name=random_country)
                driver = driver_mocker._generate_driver()
                insert_query, values = driver_mocker._create_insert_query(driver)
                db_manager._execute_query(insert_query, values)

                """Insert driver's preferences"""
                driver_preferences_mocker = DriverPreferencesMocker(driver_id=driver.driver_id, 
                                                                  country_code=f"{self.countries[random_country]}", 
                                                                  country_name=random_country)
                driver_preferences = driver_preferences_mocker._generate_driver_preference()
                insert_query, values = driver_preferences_mocker._create_insert_query(driver_preferences)
                db_manager._execute_query(insert_query, values)

                """Insert trips"""
                trips_mocker = TripMocker(country_code=f"{self.countries[random_country]}",
                                          departure_city_id=origin_city.zip_code,
                                          destination_city_id= destination_city.zip_code,
                                          driver_id=driver.driver_id)
                trip = trips_mocker._generate_trip()
                insert_query, values = trips_mocker._create_insert_query(trip)
                db_manager._execute_query(insert_query, values)

                """Insert stops"""
                if trip.number_of_stops > 0:
                    previous_stop_id=None
                    for i in range(1, trip.number_of_stops+1):
                        stops_mocker = StopMocker(country_code=f"{self.countries[random_country]}",
                                                  country_name=random_country,
                                                  trip_id=trip.trip_id,
                                                  stop_order=i,
                                                  previous_stop_id=previous_stop_id
                                                  )
                        stop, city = stops_mocker._generate_stop()
                        insert_queries = stops_mocker._create_insert_query(city, stop)
                        previous_stop_id = stop.stop_id
                        for element in insert_queries:
                            insert_query, values = element
                            db_manager._execute_query(insert_query, values)

                """Insert reservations && Passengers"""
                for i in range (1,trip.number_of_seats):
                    reservations_mocker = ReservationMocker(country_code=f"{self.countries[random_country]}",
                                                            country_name=random_country,
                                                            trip_id=trip.trip_id
                                                            )
                    reservation, passenger = reservations_mocker._generate_reservation()
                    insert_queries = reservations_mocker._create_insert_query(passenger, reservation)
                    for element in insert_queries:
                        insert_query, values = element
                        db_manager._execute_query(insert_query, values)

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            db_manager._close_connection()

PoblateDB(num_entries=40).run()