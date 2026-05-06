-- =====================================================
-- QuickBite SQL — All Exercise Solutions
-- =====================================================
-- 20 problems: 5 beginner + 5 intermediate + 5 advanced + 5 bonus.
-- Story date: 2026-04-28 (yesterday = 2026-04-27, "this month" = April 2026).
-- All solutions tested on SQLite via scripts/validate_session_queries.py.
-- =====================================================


-- =====================================================
-- BEGINNER 1: Customers signed up in 2025
-- =====================================================
SELECT COUNT(*) AS n_customers
FROM customers
WHERE signup_date >= '2025-01-01'
  AND signup_date <  '2026-01-01';


-- =====================================================
-- BEGINNER 2: Average order value this month
-- =====================================================
SELECT ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE order_date >= '2026-04-01'
  AND status = 'DELIVERED';


-- =====================================================
-- BEGINNER 3: Top 10 most expensive single orders
-- =====================================================
SELECT order_id, customer_id, restaurant_id,
       total_amount, status, order_date
FROM orders
ORDER BY total_amount DESC
LIMIT 10;


-- =====================================================
-- BEGINNER 4: Restaurants per city
-- =====================================================
SELECT city, COUNT(*) AS n_restaurants
FROM restaurants
GROUP BY city
ORDER BY n_restaurants DESC;


-- =====================================================
-- BEGINNER 5: Cancellations between 2026-04-21 and 2026-04-27
-- =====================================================
SELECT COUNT(*) AS cancelled_orders
FROM orders
WHERE status = 'CANCELLED'
  AND order_date BETWEEN '2026-04-21' AND '2026-04-27';


-- =====================================================
-- INTERMEDIATE 1: Restaurants with rating >= 4.5 AND >= 50 reviews
-- =====================================================
SELECT r.restaurant_id, r.name, r.city, r.rating_avg,
       COUNT(rt.rating_id) AS n_reviews
FROM restaurants r
JOIN orders   o  ON r.restaurant_id = o.restaurant_id
JOIN ratings  rt ON o.order_id      = rt.order_id
WHERE r.rating_avg >= 4.5
GROUP BY r.restaurant_id, r.name, r.city, r.rating_avg
HAVING COUNT(rt.rating_id) >= 50
ORDER BY r.rating_avg DESC, n_reviews DESC;


-- =====================================================
-- INTERMEDIATE 2: Customers ordering from 5+ different restaurants
-- =====================================================
SELECT c.customer_id, c.name,
       COUNT(DISTINCT o.restaurant_id) AS n_restaurants
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT o.restaurant_id) >= 5
ORDER BY n_restaurants DESC
LIMIT 20;


-- =====================================================
-- INTERMEDIATE 3: Cities ranked by total revenue this month
-- =====================================================
SELECT r.city,
       ROUND(SUM(o.total_amount), 2) AS revenue
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_date >= '2026-04-01'
  AND o.status     = 'DELIVERED'
GROUP BY r.city
ORDER BY revenue DESC;


-- =====================================================
-- INTERMEDIATE 4: Restaurants that have NEVER received an order
-- =====================================================
SELECT r.restaurant_id, r.name, r.city
FROM restaurants r
LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_id IS NULL
ORDER BY r.name;


-- =====================================================
-- INTERMEDIATE 5: Average order value per cuisine
-- =====================================================
SELECT r.cuisine,
       ROUND(AVG(o.total_amount), 2) AS avg_order_value,
       COUNT(*)                       AS n_orders
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.status = 'DELIVERED'
GROUP BY r.cuisine
ORDER BY avg_order_value DESC;


-- =====================================================
-- ADVANCED 1: Customers whose 2nd order was bigger than their 1st (LAG)
-- =====================================================
WITH numbered AS (
    SELECT customer_id,
           order_id,
           order_date,
           total_amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS order_rank,
           LAG(total_amount) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS prev_amount
    FROM orders
)
SELECT customer_id, order_id, order_date,
       total_amount,
       prev_amount,
       ROUND(total_amount - prev_amount, 2) AS diff
FROM numbered
WHERE order_rank = 2
  AND total_amount > prev_amount
ORDER BY diff DESC
LIMIT 20;


-- =====================================================
-- ADVANCED 2: Top 3 customers by total spend in each city
-- =====================================================
WITH spend AS (
    SELECT c.city, c.customer_id, c.name,
           SUM(o.total_amount) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'DELIVERED'
    GROUP BY c.city, c.customer_id, c.name
),
ranked AS (
    SELECT city, customer_id, name, total_spend,
           ROW_NUMBER() OVER (PARTITION BY city ORDER BY total_spend DESC) AS rk
    FROM spend
)
SELECT city, name, ROUND(total_spend, 2) AS total_spend
FROM ranked
WHERE rk <= 3
ORDER BY city, total_spend DESC;


-- =====================================================
-- ADVANCED 3: Month-over-month revenue growth
-- =====================================================
WITH monthly AS (
    SELECT SUBSTR(order_date, 1, 7) AS month,
           SUM(total_amount)         AS revenue
    FROM orders
    WHERE status = 'DELIVERED'
    GROUP BY SUBSTR(order_date, 1, 7)
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND(LAG(revenue) OVER (ORDER BY month), 2) AS prev_month,
       ROUND( (revenue - LAG(revenue) OVER (ORDER BY month))
              * 100.0
              / LAG(revenue) OVER (ORDER BY month), 2) AS pct_change
FROM monthly
ORDER BY month;


-- =====================================================
-- ADVANCED 4: Restaurants ranked within their cuisine by revenue
-- =====================================================
WITH rev AS (
    SELECT r.restaurant_id, r.name, r.cuisine, r.city,
           SUM(o.total_amount) AS revenue
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE o.status = 'DELIVERED'
    GROUP BY r.restaurant_id, r.name, r.cuisine, r.city
)
SELECT cuisine, name, city,
       ROUND(revenue, 2) AS revenue,
       RANK() OVER (PARTITION BY cuisine ORDER BY revenue DESC) AS rank_in_cuisine
FROM rev
ORDER BY cuisine, rank_in_cuisine
LIMIT 30;


-- =====================================================
-- ADVANCED 5: Customers with orders on 5+ consecutive days (gaps & islands)
-- =====================================================
WITH ordered_dates AS (
    SELECT DISTINCT customer_id, order_date
    FROM orders
),
streaks AS (
    SELECT customer_id, order_date,
           julianday(order_date)
             - ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS streak_id
    FROM ordered_dates
)
SELECT customer_id,
       COUNT(*)        AS streak_length,
       MIN(order_date) AS streak_start,
       MAX(order_date) AS streak_end
FROM streaks
GROUP BY customer_id, streak_id
HAVING COUNT(*) >= 5
ORDER BY streak_length DESC, streak_start
LIMIT 20;


-- =====================================================
-- BONUS 1 (P1): Most-used promo code this month
-- =====================================================
SELECT p.promo_code,
       COUNT(*)                       AS times_used,
       ROUND(SUM(o.total_amount), 2)  AS revenue
FROM orders o
JOIN promotions p ON o.promo_id = p.promo_id
WHERE o.order_date >= '2026-04-01'
  AND o.status     = 'DELIVERED'
GROUP BY p.promo_code
ORDER BY times_used DESC
LIMIT 10;


-- =====================================================
-- BONUS 2 (P2): Average delivery time per city
-- =====================================================
SELECT dp.city,
       ROUND(AVG((JULIANDAY(da.delivery_time) - JULIANDAY(da.pickup_time)) * 1440), 1) AS avg_delivery_min,
       COUNT(*) AS n_completed
FROM delivery_assignments da
JOIN delivery_partners   dp ON da.partner_id = dp.partner_id
WHERE da.delivery_status = 'COMPLETED'
GROUP BY dp.city
ORDER BY avg_delivery_min;


-- =====================================================
-- BONUS 3 (P3): Top 5 delivery partners by completed deliveries
-- =====================================================
SELECT dp.partner_id, dp.name, dp.city, dp.vehicle,
       COUNT(*) AS completed_deliveries
FROM delivery_assignments da
JOIN delivery_partners   dp ON da.partner_id = dp.partner_id
WHERE da.delivery_status = 'COMPLETED'
GROUP BY dp.partner_id, dp.name, dp.city, dp.vehicle
ORDER BY completed_deliveries DESC
LIMIT 5;


-- =====================================================
-- BONUS 4 (P4): Orders that used an EXPIRED promo code (data quality check)
-- =====================================================
SELECT o.order_id, o.order_date,
       p.promo_code, p.valid_until
FROM orders o
JOIN promotions p ON o.promo_id = p.promo_id
WHERE o.order_date > p.valid_until
ORDER BY o.order_date DESC
LIMIT 20;


-- =====================================================
-- BONUS 5 (P5): Distance bucket vs avg delivery time
-- =====================================================
SELECT CASE
           WHEN distance_km < 2 THEN '0-2 km'
           WHEN distance_km < 4 THEN '2-4 km'
           WHEN distance_km < 6 THEN '4-6 km'
           WHEN distance_km < 8 THEN '6-8 km'
           ELSE '8+ km'
       END AS distance_bucket,
       COUNT(*) AS n_deliveries,
       ROUND(AVG((JULIANDAY(delivery_time) - JULIANDAY(pickup_time)) * 1440), 1) AS avg_delivery_min
FROM delivery_assignments
WHERE delivery_status = 'COMPLETED'
GROUP BY distance_bucket
ORDER BY distance_bucket;
