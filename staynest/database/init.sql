-- ============================================================
--  StayNest Database Initialization
--  Three-Tier Application — MySQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS staynest;
USE staynest;

-- ─────────────────────────────────────────
--  TABLE: users
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id          INT          AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('guest','host') NOT NULL DEFAULT 'guest',
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_users_email (email)
);

-- ─────────────────────────────────────────
--  TABLE: properties
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS properties (
    id          INT           AUTO_INCREMENT PRIMARY KEY,
    host_id     INT           NOT NULL,
    name        VARCHAR(200)  NOT NULL,
    description TEXT,
    location    VARCHAR(255)  NOT NULL,
    price       DECIMAL(10,2) NOT NULL,
    bedrooms    INT           NOT NULL DEFAULT 1,
    guests      INT           NOT NULL DEFAULT 2,
    image_url   VARCHAR(500),
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_properties_host (host_id)
);

-- ─────────────────────────────────────────
--  TABLE: bookings
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bookings (
    id          INT           AUTO_INCREMENT PRIMARY KEY,
    user_id     INT           NOT NULL,
    property_id INT           NOT NULL,
    check_in    DATE          NOT NULL,
    check_out   DATE          NOT NULL,
    guests      INT           NOT NULL DEFAULT 1,
    total_price DECIMAL(10,2) NOT NULL,
    status      ENUM('pending','confirmed','cancelled') NOT NULL DEFAULT 'pending',
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id)  ON DELETE CASCADE,
    INDEX idx_bookings_user     (user_id),
    INDEX idx_bookings_property (property_id)
);

-- ─────────────────────────────────────────
--  SEED DATA — demo host + guest + properties
-- ─────────────────────────────────────────

-- Password for both demo accounts: "password123"
-- Hash generated with bcrypt cost-12
INSERT IGNORE INTO users (name, email, password, role) VALUES
(
    'Demo Host',
    'host@staynest.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaJObDyWcJcQ4F1eZMGKIeHmy',
    'host'
),
(
    'Demo Guest',
    'guest@staynest.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaJObDyWcJcQ4F1eZMGKIeHmy',
    'guest'
);

-- Demo properties (host_id = 1)
INSERT IGNORE INTO properties (host_id, name, description, location, price, bedrooms, guests, image_url) VALUES
(
    1,
    'Cozy Beach House',
    'A beautiful beachfront property with stunning ocean views. Perfect for a relaxing getaway. Enjoy sunsets from the private deck, walk to the beach in minutes, and unwind in a fully equipped home.',
    'Goa, India',
    4500.00,
    2,
    4,
    'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=800&q=80'
),
(
    1,
    'Mountain Retreat Cabin',
    'Escape to the mountains in this charming wooden cabin surrounded by pine trees. Ideal for couples and small families who love nature, hiking, and fresh mountain air.',
    'Manali, Himachal Pradesh',
    3200.00,
    1,
    2,
    'https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?w=800&q=80'
),
(
    1,
    'Heritage City Apartment',
    'A tastefully decorated apartment in the heart of the old city. Walking distance to museums, restaurants, and local markets. Great base for city exploration.',
    'Jaipur, Rajasthan',
    2800.00,
    2,
    3,
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80'
),
(
    1,
    'Luxury Villa with Pool',
    'Indulge in this stunning villa featuring a private swimming pool, lush garden, and spacious interiors. Ideal for groups and families looking for a premium experience.',
    'Udaipur, Rajasthan',
    9500.00,
    4,
    8,
    'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800&q=80'
),
(
    1,
    'Backwater Houseboat',
    'Experience the famous Kerala backwaters from a traditional wooden houseboat. Includes meals, guided boat tours, and breathtaking scenic views.',
    'Alleppey, Kerala',
    6000.00,
    2,
    4,
    'https://images.unsplash.com/photo-1578645510447-e20b4311e3ce?w=800&q=80'
),
(
    1,
    'Forest Eco Cottage',
    'An eco-friendly cottage nestled deep in the forest. Solar-powered, with organic meals and guided nature walks. Perfect for those seeking peace and sustainability.',
    'Coorg, Karnataka',
    3800.00,
    1,
    2,
    'https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=800&q=80'
);
