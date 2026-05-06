-- =====================================================
-- QuickBite SQL — PostgreSQL DDL
-- =====================================================
-- Use this with psql + COPY FROM to load the CSVs:
--   createdb quickbite
--   psql quickbite -f scripts/schema.sql
--   psql quickbite -c "\copy cities FROM 'data/cities.csv' WITH CSV HEADER"
--   ... (repeat for each table)
-- See run_locally.md for the full sequence.
-- =====================================================

DROP TABLE IF EXISTS delivery_assignments;
DROP TABLE IF EXISTS delivery_partners;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS promotions;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS cities;


CREATE TABLE cities (
    city_id        TEXT PRIMARY KEY,
    city_name      TEXT NOT NULL,
    state          TEXT NOT NULL,
    latitude       DOUBLE PRECISION,
    longitude      DOUBLE PRECISION,
    tier           TEXT,
    launched_date  DATE
);

CREATE TABLE customers (
    customer_id    TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    email          TEXT,
    city           TEXT,
    signup_date    DATE,
    age            INTEGER
);

CREATE TABLE restaurants (
    restaurant_id   TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    city            TEXT,
    cuisine         TEXT,
    rating_avg      NUMERIC(3,1),
    price_tier      TEXT,
    onboarded_date  DATE,
    is_active       INTEGER
);

CREATE TABLE promotions (
    promo_id            TEXT PRIMARY KEY,
    promo_code          TEXT,
    discount_type       TEXT,
    discount_value      NUMERIC,
    min_order_value     NUMERIC,
    valid_from          DATE,
    valid_until         DATE,
    applicable_cuisine  TEXT,
    max_uses            INTEGER
);

CREATE TABLE orders (
    order_id        TEXT PRIMARY KEY,
    customer_id     TEXT REFERENCES customers(customer_id),
    restaurant_id   TEXT REFERENCES restaurants(restaurant_id),
    order_date      DATE,
    order_time      TEXT,
    total_amount    NUMERIC(10,2),
    status          TEXT,
    promo_id        TEXT REFERENCES promotions(promo_id),
    payment_method  TEXT
);

CREATE TABLE order_items (
    order_id     TEXT REFERENCES orders(order_id),
    item_name    TEXT,
    quantity     INTEGER,
    item_price   NUMERIC(10,2)
);

CREATE TABLE ratings (
    rating_id    TEXT PRIMARY KEY,
    order_id     TEXT REFERENCES orders(order_id),
    stars        INTEGER,
    review_text  TEXT,
    rated_at     TIMESTAMP
);

CREATE TABLE delivery_partners (
    partner_id   TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    city         TEXT,
    vehicle      TEXT,
    joined_date  DATE,
    is_active    INTEGER
);

CREATE TABLE delivery_assignments (
    assignment_id    TEXT PRIMARY KEY,
    order_id         TEXT REFERENCES orders(order_id),
    partner_id       TEXT REFERENCES delivery_partners(partner_id),
    pickup_time      TIMESTAMP,
    delivery_time    TIMESTAMP,
    delivery_status  TEXT,
    distance_km      NUMERIC(5,2)
);


-- Indexes (optional but useful for the session queries)
CREATE INDEX idx_orders_date          ON orders(order_date);
CREATE INDEX idx_orders_customer      ON orders(customer_id);
CREATE INDEX idx_orders_restaurant    ON orders(restaurant_id);
CREATE INDEX idx_orders_status        ON orders(status);
CREATE INDEX idx_ratings_order        ON ratings(order_id);
CREATE INDEX idx_assignments_partner  ON delivery_assignments(partner_id);
CREATE INDEX idx_order_items_order    ON order_items(order_id);
