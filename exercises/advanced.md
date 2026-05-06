# Advanced exercises

5 problems covering CTEs, window functions, subqueries, and complex date logic. Solutions in [`../solutions/all_solutions.sql`](../solutions/all_solutions.sql).

These are the kind of questions a senior analyst gets — non-trivial, but each breaks down into a clean CTE chain.

---

## A1 — Customers whose 2nd order was bigger than their 1st (use `LAG`)

For each customer with at least 2 orders, compare order #2 to order #1. Return customers where the second order's `total_amount` exceeded the first.

Show `customer_id`, `order_id` of the second order, `total_amount`, the previous (first) `total_amount`, and the difference. Top 20 by difference.

> Hint: `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id)` to number orders per customer; `LAG(total_amount)` to grab the previous order's amount; then filter to `row_number = 2 AND total_amount > prev_amount`.

---

## A2 — Top 3 customers by total spend in each city

Per city, the 3 customers with the highest total `total_amount` from delivered orders.

> Hint: build a `spend` CTE (city, customer, total_spend), then `ROW_NUMBER() OVER (PARTITION BY city ORDER BY total_spend DESC)`, then filter to `rk <= 3`.

---

## A3 — Month-over-month revenue growth

For each calendar month in the data, total delivered revenue plus the **percent change** vs the previous month.

> Hint: `SUBSTR(order_date, 1, 7)` gets the `YYYY-MM` prefix in SQLite. Use `LAG(revenue) OVER (ORDER BY month)` to grab the prior month's revenue; then `(curr - prev) * 100.0 / prev`.

---

## A4 — Restaurants ranked within their cuisine by revenue

For each restaurant, its total delivered revenue. Then **rank within cuisine** so we can see "the #1 Biryani place", "the #1 Pizza place", etc. Show the top 30 rows overall, ordered by cuisine then rank.

> Hint: `RANK() OVER (PARTITION BY cuisine ORDER BY revenue DESC)`. Use `RANK` (not `ROW_NUMBER`) so genuine ties don't get arbitrarily resolved.

---

## A5 — Customers with orders on 5+ consecutive days

Find customers who placed at least one order on 5 or more **consecutive calendar days** in a row.

> Hint: this is the classic "gaps and islands" pattern. For each customer's distinct order dates, subtract `ROW_NUMBER()` (in date order) from the date itself. Consecutive dates produce the same difference — so you can `GROUP BY (date - row_number)` and `HAVING COUNT(*) >= 5` to find streaks.

In SQLite, use `julianday(order_date) - ROW_NUMBER() ...` because `julianday` is numeric and supports subtraction.
