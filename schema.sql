-- Crear tabla User
CREATE TABLE [User] (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla City
CREATE TABLE City (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50),
    country_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_code) REFERENCES Country(code)
);

-- Crear tabla Country
CREATE TABLE Country (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla Place
CREATE TABLE Place (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    host_id VARCHAR(36),
    city_id VARCHAR(36),
    number_of_rooms INT,
    number_of_bathrooms INT,
    max_guests INT,
    price_per_night INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES [User](id),
    FOREIGN KEY (city_id) REFERENCES City(id)
);

-- Crear tabla Review
CREATE TABLE Review (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    place_id VARCHAR(36),
    comment TEXT,
    rating FLOAT CHECK(rating BETWEEN 0 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES [User](id),
    FOREIGN KEY (place_id) REFERENCES Place(id)
);

-- Crear tabla Amenitypytest

CREATE TABLE Amenity (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla PlaceAmenity (relación muchos a muchos)
CREATE TABLE PlaceAmenity (
    place_id VARCHAR(36),
    amenity_id VARCHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);
