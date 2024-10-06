CREATE TABLE IF NOT EXISTS public.driver (
    driver_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    phone VARCHAR(25),
    rating DECIMAL(3, 2) DEFAULT 0.0 CHECK (rating >= 0.00 AND rating <= 5.00),
    is_id_verified BOOLEAN DEFAULT FALSE,
    cancellation_record VARCHAR(20) CHECK (cancellation_record IN ('Rarely Cancels', 'Usually Cancels', 'Never Cancels'))
);

CREATE TABLE IF NOT EXISTS public.driver_preferences (
    driver_id UUID PRIMARY KEY REFERENCES driver(driver_id) ON DELETE CASCADE,
    about_me VARCHAR(255) NOT NULL,
    total_rides_published SMALLINT NOT NULL,
    member_since DATE CHECK (member_since <= CURRENT_DATE),
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_phone_verified BOOLEAN DEFAULT FALSE,
    chattiness VARCHAR(250) NOT NULL CHECK (chattiness IN ('Chatty when comfortable', 'Quiet', 'Im a chatterbox')),
    music VARCHAR(250) NOT NULL CHECK (music IN ('Depends on mood', 'No music', 'Always music', 'Its all about the playlist')),
    smoking BOOLEAN DEFAULT FALSE,
    pets VARCHAR(250) NOT NULL CHECK (pets IN ('Depends on the animal', 'No pets', 'All pets allowed'))
);

CREATE TABLE IF NOT EXISTS public.city (
    city_id SERIAL PRIMARY KEY, -- insertado desde postgres
    city_name VARCHAR(100) NOT NULL UNIQUE,
    zip_code VARCHAR(10) UNIQUE,
    country VARCHAR(50),
    UNIQUE (city_name, zip_code)
);

CREATE TABLE IF NOT EXISTS public.trip (
    trip_id UUID PRIMARY KEY, -- insert it from the backend
    driver_id UUID REFERENCES driver(driver_id) ON DELETE SET NULL,
    departure_city_id VARCHAR(10) REFERENCES city(zip_code) ON DELETE SET NULL,
    destination_city_id VARCHAR(10) REFERENCES city(zip_code) ON DELETE SET NULL,
    departure_date_time TIMESTAMP NOT NULL,
    number_of_stops INT NOT NULL,
    number_of_seats INT NOT NULL,
    price_per_seat DECIMAL(10, 2) NOT NULL,
    women_only BOOLEAN DEFAULT FALSE,
    enabled_instant_booking BOOLEAN DEFAULT FALSE,
    total_distance_km DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('scheduled', 'ongoing', 'completed', 'cancelled')) NOT NULL DEFAULT 'scheduled',
    additional_comments TEXT
);

CREATE TABLE IF NOT EXISTS public.stop (
    stop_id UUID PRIMARY KEY, -- insert it from the backend
    trip_id UUID REFERENCES trip(trip_id) ON DELETE CASCADE,
    city_id INT REFERENCES city(city_id) ON DELETE SET NULL,
    stop_order INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    distance_km DECIMAL(10, 2) NOT NULL,
    estimated_arrival_time TIMESTAMP NOT NULL,
    previous_stop_id UUID REFERENCES stop(stop_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS public.passenger (
    passenger_id UUID PRIMARY KEY, -- insert it from the backend
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    rating DECIMAL(3, 2) DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS public.reservation (
    reservation_id UUID PRIMARY KEY, -- insert it from the backend
    trip_id UUID REFERENCES trip(trip_id) ON DELETE CASCADE,
    passenger_id UUID REFERENCES passenger(passenger_id) ON DELETE CASCADE,
    reservation_date_time TIMESTAMP NOT NULL,
    price_paid DECIMAL(10, 2) NOT NULL
);
