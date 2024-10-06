from faker import Faker
from typing import List, Tuple
from entities.models import *


class CityMocker:
    def __init__(self, country_code: str, country_name: str) -> None:
        self._faker = Faker(country_code)
        self._country = country_name

    def _generate_cities(self) -> Tuple[City, City]:
        city_name = self._faker.city()
        zip_code = self._faker.postcode() 
        nearby_city_name = self._faker.city()
        nearby_zip_code = self._faker.postcode()

        city1 = City(city_name=city_name, zip_code=zip_code, country=self._country)
        city2 = City(city_name=nearby_city_name, zip_code=nearby_zip_code, country=self._country)

        return city1, city2

    def _create_insert_query(self, cities: List[City]) -> List[Tuple[str, Tuple]]:
        """Generate separate insert queries for each city."""
        insert_queries = []
        
        for city in cities:
            insert_query = """
            INSERT INTO public.city (city_name, zip_code, country)
            VALUES (%s, %s, %s)
            ON CONFLICT (city_name, zip_code) DO NOTHING;
            """
            values = (city.city_name, city.zip_code, city.country)
            insert_queries.append((insert_query, values))
        
        return insert_queries
