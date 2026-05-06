# Beginner exercises

5 problems covering `SELECT`, `WHERE`, aggregates (`COUNT`, `SUM`, `AVG`), `ORDER BY`, and `LIMIT`. No joins, no grouping. Try each one before peeking at the solutions in [`../solutions/all_solutions.sql`](../solutions/all_solutions.sql).

The story date is **2026-04-28** ("today"), so "this month" means April 2026 and "yesterday" means 2026-04-27.

---

## B1 — Customers signed up in 2025

How many customers have a `signup_date` somewhere in calendar year 2025?

> Hint: filter `signup_date` between `'2025-01-01'` and `'2025-12-31'` (inclusive on both sides), or use `>=` and `<` with `'2026-01-01'`.

---

## B2 — Average order value this month

Among **delivered** orders placed in April 2026, what is the average `total_amount`? Round to 2 decimal places.

> Hint: `AVG(total_amount)` plus a `WHERE` on `order_date` and `status`.

---

## B3 — Top 10 most expensive single orders

Show the 10 individual orders with the highest `total_amount`. Include `order_id`, `customer_id`, `restaurant_id`, `total_amount`, `status`, and `order_date`.

> Hint: `ORDER BY total_amount DESC LIMIT 10`. No filtering needed — any status, any date.

---

## B4 — Restaurants per city

How many restaurants are in each city? Sort by city size, largest first.

> Hint: `GROUP BY city`. (Yes, this is technically a GROUP BY — but you've seen it in the notebook.)

---

## B5 — Cancellations this week

How many orders were **cancelled** between 2026-04-21 and 2026-04-27 (inclusive)?

> Hint: `WHERE status = 'CANCELLED' AND order_date BETWEEN ... AND ...`.
