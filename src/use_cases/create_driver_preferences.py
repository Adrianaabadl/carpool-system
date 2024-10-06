from faker import Faker
import random
from typing import List
from entities.models import *

class DriverPreferencesMocker:
    def __init__(self, country_code: str, country_name, driver_id) -> None:
        self._faker = Faker(country_code)
        self._country = country_name
        self._driver_id = driver_id 

    def _generate_driver_preference(self) -> DriverPreferences:
        about_me = self._faker.sentence(nb_words=10)
        total_rides_published = random.randint(0, 500)
        member_since = self._faker.date_this_decade(before_today=True, after_today=False)
        is_email_verified = random.choice([True, False])
        is_phone_verified = random.choice([True, False])
        chattiness = random.choice(['Chatty when comfortable', 'Quiet', 'Im a chatterbox'])
        music = random.choice(['Depends on mood', 'No music', 'Always music', 'Its all about the playlist'])
        smoking = random.choice([True, False])
        pets = random.choice(['Depends on the animal', 'No pets', 'All pets allowed'])

        return DriverPreferences(
            driver_id = self._driver_id,
            about_me=about_me,
            total_rides_published=total_rides_published,
            member_since=member_since,
            is_email_verified=is_email_verified,
            is_phone_verified=is_phone_verified,
            chattiness=chattiness,
            music=music,
            smoking=smoking,
            pets=pets
        )

    def _generate_driver_preferences_list(self, num_preferences: int) -> List[DriverPreferences]:
        preferences = []
        for driver_id in range(1, num_preferences + 1):
            preference = self._generate_driver_preference(driver_id)
            preferences.append(preference)
        return preferences

    def _create_insert_query(self, driver_preference: DriverPreferences):
        insert_query = """
        INSERT INTO public.driver_preferences (driver_id, about_me, total_rides_published, member_since, 
                                              is_email_verified, is_phone_verified, chattiness, music, smoking, pets)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            driver_preference.driver_id,
            driver_preference.about_me,
            driver_preference.total_rides_published,
            driver_preference.member_since,
            driver_preference.is_email_verified,
            driver_preference.is_phone_verified,
            driver_preference.chattiness,
            driver_preference.music,
            driver_preference.smoking,
            driver_preference.pets
        )
        return insert_query, values
