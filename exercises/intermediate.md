# Intermediate exercises

5 problems covering `GROUP BY`, `HAVING`, `INNER JOIN`, and `LEFT JOIN`. Solutions in [`../solutions/all_solutions.sql`](../solutions/all_solutions.sql).

The story date is **2026-04-28** ("today"). "This month" = April 2026.

---

## I1 — Restaurants with rating ≥ 4.5 AND ≥ 50 reviews

Find restaurants where:
- `restaurants.rating_avg >= 4.5`, **and**
- They have at least 50 rows in the `ratings` table

Show `restaurant_id`, `name`, `city`, `rating_avg`, and the review count. Order by rating then review count, both descending.

> Hint: `restaurants → orders → ratings` is the join path. Use `HAVING COUNT(rt.rating_id) >= 50`.

---

## I2 — Customers ordering from 5+ different restaurants

Customers who have placed orders at **at least 5 distinct restaurants** (any time, any status).

Show `customer_id`, `name`, and the distinct restaurant count. Top 20 by count.

> Hint: `COUNT(DISTINCT restaurant_id)` plus `HAVING`.

---

## I3 — Cities ranked by total revenue this month

For each city, the total revenue from **delivered** orders in April 2026. Highest revenue first.

> Hint: this is the same shape as Q4 in the notebook, but with a wider date window.

---

## I4 — Restaurants that have NEVER received an order

Use a `LEFT JOIN` from `restaurants` to `orders`, then keep only rows where the `orders` side is `NULL`.

> Hint: `WHERE o.order_id IS NULL` after the LEFT JOIN. Show `restaurant_id`, `name`, `city`.

---

## I5 — Average order value per cuisine

For each cuisine, the average `total_amount` of delivered orders, plus the order count.

> Hint: join `orders` to `restaurants`, group by `cuisine`. Sort by avg DESC.
