# Bonus exercises — promotions, delivery, cities

5 problems that exercise the four "supporting" tables (`promotions`, `delivery_partners`, `delivery_assignments`, `cities`). Solutions in [`../solutions/all_solutions.sql`](../solutions/all_solutions.sql).

---

## P1 — Most-used promo code this month

For April 2026 delivered orders, which promo codes were used most? Show `promo_code`, the count, and the revenue. Top 10.

> Hint: join `orders` to `promotions` on `promo_id`. Filter `o.order_date >= '2026-04-01' AND o.status = 'DELIVERED'`. Group by `promo_code`.

---

## P2 — Average delivery time per city

For completed deliveries, what's the average minutes between `pickup_time` and `delivery_time`, grouped by the **delivery partner's** city?

> Hint: `(JULIANDAY(delivery_time) - JULIANDAY(pickup_time)) * 1440` gives minutes in SQLite. Join `delivery_assignments` to `delivery_partners`. Filter `delivery_status = 'COMPLETED'`.

---

## P3 — Top 5 delivery partners by completed deliveries

Which 5 partners completed the most deliveries? Show `partner_id`, `name`, `city`, `vehicle`, and the count.

> Hint: same join as P2, but group by partner and sort descending.

---

## P4 — Orders that used an EXPIRED promo code (data quality check)

A real bug: find orders where the `order_date` is **after** the promo's `valid_until`. These shouldn't have been allowed but slipped through.

Show `order_id`, `order_date`, `promo_code`, and `valid_until`.

> Hint: simple `WHERE o.order_date > p.valid_until` after a join.

---

## P5 — Distance vs delivery time

Bucket completed deliveries by `distance_km` (`0–2`, `2–4`, `4–6`, `6–8`, `8+ km`) and show the average delivery minutes per bucket. Does longer distance correlate with longer delivery time?

> Hint: `CASE WHEN` to make the bucket label, then `GROUP BY` it. SQLite has no `CORR()`, so this bucketing is a clean way to show the relationship visually in the result.
