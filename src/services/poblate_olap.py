import psycopg2
from google.cloud import bigquery
from infrastructure.database import DbManager

class PoblateDB:
    def __init__(self) -> None:
        self._bq_client = bigquery.Client()
        self.db_manager = DbManager()
        self.db_manager._create_connection()

    def run(self):
        try:
            # self.insert_drivers()
            # self.insert_passengers()
            # self.insert_trips()
            self.insert_reservations()

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.db_manager._close_connection()

    def insert_drivers(self):
        query = """SELECT 
                d.driver_id, 
                d.name, 
                d.is_id_verified, 
                d.rating, 
                dp.total_rides_published, 
                dp.member_since 
            FROM public.driver d 
            LEFT JOIN public.driver_preferences dp ON dp.driver_id = d.driver_id
        """
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


    def insert_passengers(self):
        query = "SELECT passenger_id, name, rating FROM public.passenger"
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

    def insert_trips(self):
        query = """SELECT 
                t.trip_id,
                t.driver_id,
                dep.city_name AS departure_city,
                dest.city_name AS destination_city,
                dest.country AS destination_country,
                t.departure_date_time,
                t.number_of_stops,
                t.number_of_seats,
                t.total_distance_km 
            FROM trip t
            JOIN city dep ON t.departure_city_id = dep.zip_code
            JOIN city dest ON t.destination_city_id = dest.zip_code
            WHERE t.status = 'completed'        
        """
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


    def insert_reservations(self):
        query = "SELECT reservation_id, trip_id, passenger_id, reservation_date_time, price_paid FROM public.reservation"
        reservations = self.db_manager.fetch_query(query)
        rows_to_insert = [
            {
                "reservation_id": reservation['reservation_id'],
                "trip_id": reservation['trip_id'],
                "passenger_id": reservation['passenger_id'],
                "reservation_date_time": reservation['reservation_date_time'],
                "price_paid": reservation['price_paid'],
            }
            for reservation in reservations
        ]

        table_id = 'develop-431503.carpool_engine.fact_reservation'
        errors = self._bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting reservations: {errors}")
        else:
            print("Reservations inserted successfully.")

populator = PoblateDB()
populator.run()
