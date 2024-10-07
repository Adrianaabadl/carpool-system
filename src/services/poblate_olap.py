import os
from google.cloud import bigquery
from infrastructure.database import DbManager

class PoblateOlap:
    def __init__(self) -> None:
        self._bq_client = bigquery.Client()
        self.db_manager = DbManager()
        self.db_manager._create_connection()
    
    def _load_query(self, filename):
        base_path = os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'transformations')
        file_path = os.path.join(base_path, filename)
        with open(file_path, 'r') as file:
            return file.read()


    def run(self):
        try:
            self._insert_drivers()
            self._insert_passengers()
            self._insert_trips()
            self._insert_reservations()

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.db_manager._close_connection()

    def _insert_drivers(self):
        query = self._load_query('dim_driver.sql')
        drivers = self.db_manager.fetch_query(query)
        rows_to_insert = [
            {
                "driver_id": str(driver['driver_id']),
                "name": driver['name'],
                "is_id_verified": driver['is_id_verified'],
                "rating": float(driver['rating']) if driver['rating'] is not None else None,
                "total_rides_published": driver['total_rides_published'] if driver['total_rides_published'] is not None else None,
                "member_since": driver['member_since'].strftime('%Y-%m-%d') if driver['member_since'] is not None else None
            }
            for driver in drivers
        ]
        table_id = 'develop-431503.carpool_engine.dim_driver'
        errors = self._bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting drivers: {errors}")
        else:
            print("Drivers inserted successfully.")


    def _insert_passengers(self):
        query = self._load_query('dim_passenger.sql')
        passengers = self.db_manager.fetch_query(query)
        rows_to_insert = [
            {
                "passenger_id": passenger['passenger_id'],
                "name": passenger['name'],
                "rating": float(passenger['rating']) if passenger['rating'] is not None else None
            }
            for passenger in passengers
        ]
        table_id = 'develop-431503.carpool_engine.dim_passenger'
        errors = self._bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting passengers: {errors}")
        else:
            print("Passengers inserted successfully.")

    def _insert_trips(self):
        query = self._load_query('dim_trip.sql')
        trips = self.db_manager.fetch_query(query)
        rows_to_insert = [
            {
                "trip_id": str(trip['trip_id']),
                "driver_id": str(trip['driver_id']),
                "departure_city": trip['departure_city'],
                "destination_city": trip['destination_city'],
                "destination_country": trip['destination_country'],
                "departure_date_time": trip['departure_date_time'].isoformat() if trip['departure_date_time'] is not None else None,
                "number_of_stops": trip['number_of_stops'],
                "number_of_seats": trip['number_of_seats'],
                "total_distance_km": float(trip['total_distance_km']) if trip['total_distance_km'] is not None else None,
            }
            for trip in trips
        ]

        table_id = 'develop-431503.carpool_engine.dim_trip'
        errors = self._bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting trips: {errors}")
        else:
            print("Trips inserted successfully.")


    def _insert_reservations(self):
        query = self._load_query('fact_reservation.sql')
        reservations = self.db_manager.fetch_query(query)
        rows_to_insert = [
            {
                "reservation_id": reservation['reservation_id'],
                "trip_id": reservation['trip_id'],
                "passenger_id": reservation['passenger_id'],
                "reservation_date_time": reservation['reservation_date_time'].isoformat() if reservation['reservation_date_time'] is not None else None,
                "price_paid": float(reservation['price_paid']) if reservation['price_paid'] is not None else None
            }
            for reservation in reservations
        ]
        table_id = 'develop-431503.carpool_engine.fact_reservation'
        errors = self._bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting reservations: {errors}")
        else:
            print("Reservations inserted successfully.")