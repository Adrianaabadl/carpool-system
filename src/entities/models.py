from datetime import date, datetime
from typing import Literal
from typing import Optional
from dataclasses import dataclass

@dataclass
class Driver:
    driver_id: str
    name: str
    email: str
    date_of_birth: date 
    phone: str
    rating: float
    is_id_verified: bool
    cancellation_record: str


@dataclass
class DriverPreferences:
    driver_id: str
    about_me: str
    total_rides_published: int
    member_since: date
    chattiness: Literal['Chatty when comfortable', 'Quiet', 'Im a chatterbox']
    music: Literal['Depends on mood', 'No music', 'Always music', 'Its all about the playlist']
    pets: Literal['Depends on the animal', 'No pets', 'All pets allowed']
    is_email_verified: bool = False
    is_phone_verified: bool = False
    smoking: bool = False


@dataclass
class City:
    city_name: str
    zip_code: str
    country: str


@dataclass
class Trip:
    trip_id: str
    driver_id: int
    departure_city_id: int
    destination_city_id: int
    departure_date_time: datetime
    number_of_stops: int
    number_of_seats: int
    price_per_seat: float
    total_distance_km: float
    status: Literal['scheduled', 'ongoing', 'completed', 'cancelled']
    women_only: Optional[bool] = False
    enabled_instant_booking: Optional[bool] = False
    additional_comments: Optional[str] = None


@dataclass
class Stop:
    stop_id: str
    trip_id: int
    city_id: int
    stop_order: int
    price: float
    distance_km: float
    estimated_arrival_time: datetime
    previous_stop_id: str


@dataclass
class Reservation:
    reservation_id: int
    trip_id: int
    passenger_id: int
    reservation_date_time: datetime
    price_paid: float


@dataclass
class Passenger:
    passenger_id: str
    name: str
    email: str
    phone: str
    rating: float = 0.0