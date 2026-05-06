# Facilitator speech — QuickBite SQL session (online, screen-share edition)

A 60-minute spoken script for delivering this session **online** (Zoom / Teams / Meet) where **only the facilitator runs the notebook on shared screen**. The audience watches and listens — they do not have the notebook open, do not run any queries, and do not type along.

**Format assumptions:**
- Audience is muted throughout. Save real Q&A for the last 5 minutes.
- The full 60 minutes is teaching time. No "everyone open Colab" preamble. No "run this cell now" pauses. No "did it work for you" check-ins.
- ~55–58 minutes of speaking, with brief pauses while queries execute on screen.
- Lines in `[brackets]` are stage cues for you (the facilitator), not spoken aloud.

**Pre-session checklist (10 minutes before going live):**
1. Open the Colab notebook in your browser. Run the setup cell. Wait for the green tick and `Ready` message.
2. Run **every query in the notebook once**, top to bottom. This pre-warms the data and makes sure each cell already has output. If you re-run during the session, results return instantly.
3. Set your screen-share to a single window mode showing only the notebook — not your full desktop. Hide bookmarks bars and tab strips.
4. Zoom the notebook to ~125% so attendees on phones can read the SQL clearly.
5. Have the repo link copy-pasted somewhere — you'll drop it in chat at the very start, and again at the close.
6. Have water nearby. You will be talking for ~55 minutes continuously.

---

## [0:00 – 0:01] Hello and the deal

> "Hi everyone, welcome. I'm dropping the repo link in chat right now — bookmark it, you'll want it after we wrap up. Today I'm going to teach you SQL through a story. You're a brand-new data analyst at a food delivery company called QuickBite. Your CEO walks up to your desk this morning and asks you nine questions, one after another, over the next hour. Each question forces you to learn one new piece of SQL. By the end, you'll have used SELECT, WHERE, JOIN, GROUP BY, CTEs, and window functions. Nine concepts. Nine questions. One hour. Save your questions for the very end — we have five minutes for Q&A. Watch my screen, follow along. Let's start."

---

## [0:01 – 0:11] 🎬 Act 1 — Simple questions

**What we're learning:** how to read a single table — `SELECT`, `FROM`, `WHERE`, and the simplest aggregates `COUNT` and `SUM`. By the end of Act 1, you'll have seen three queries written and executed.

> "Scene one. It's Tuesday morning. You've just opened your laptop. Coffee in hand. Priya — your CEO — walks up to your desk and says, _'Quick one. How did we do yesterday? Just give me the numbers.'_"
>
> "Yesterday in our story is **2026-04-27**. Priya wants three things: how many orders we got, how many of those actually got delivered, and how much revenue we made. Three questions, three queries. Let's tackle them one at a time."
>
> "Before we touch the SQL, here's the single most important idea in this whole session, and please commit it to memory: **SQL is just a way of asking questions of a table.** That's the entire game. The grammar looks a little different from English, but you're really just saying 'show me X from Y where Z'. If you hold that mental model in your head, you'll never feel lost. Everything we do for the next hour is variations on that one shape — show me X from Y where Z."

### Q1 — How many orders yesterday?

> [scroll to Q1 cell]
>
> "Here's our first query. Three lines. Read it like English with me: `SELECT COUNT-of-everything FROM orders WHERE order_date equals 2026-04-27`. Three ideas in one sentence — what to show, where to look, how to filter. Every SQL query you'll ever write follows this shape, just with more pieces glued on as the questions get more complex."
>
> "Let me walk through the syntax line by line, because the line-by-line is the part most tutorials skip past."
>
> "Line one: `SELECT COUNT(*) AS total_orders`. The `SELECT` keyword tells SQL 'I'm asking for the following columns'. `COUNT(*)` is a function that counts how many rows come out at the end. The star inside means 'count every row, don't worry about which specific column'. The `AS total_orders` part renames the output column — without it, SQL would label the column with the literal text `COUNT(*)`, which looks ugly when you display the result. So `AS` just gives the result a friendly, human-readable name. Aliases like this show up everywhere in SQL; we'll use them on tables in a few minutes too."
>
> "Line two: `FROM orders`. That's the table we're querying. SQL looks at the `orders` table — and only the `orders` table — for the rest of the query."
>
> "Line three: `WHERE order_date = '2026-04-27'`. This is the filter. Two things to notice. One — the equals sign is just a single equals, not double like in Python or JavaScript. Single equals in SQL means comparison. Two — the date is wrapped in single quotes, because dates in SQL are treated as text strings in the SQLite dialect. If you write `WHERE order_date = 2026-04-27` without quotes, SQL will try to do the math `2026 minus 4 minus 27`, get the number `1995`, and compare that to the date column — which won't match anything. Common, common mistake. Always quote your date literals."
>
> [run the cell, wait 2 seconds for the result]
>
> "And there's our answer: 900 orders yesterday. Priya is happy. She has her first number."

### Concept deep-dive — how SQL actually evaluates a query

> "Quick tangent before query two. This is one of those things nobody teaches you on day one, but it explains a lot of behavior you'll run into later, so let me drop it in early."
>
> "SQL queries are written in one order but **evaluated in a different order**. When you read `SELECT COUNT(*) FROM orders WHERE order_date = '2026-04-27'`, your brain reads top to bottom — `SELECT` first, `FROM` second, `WHERE` third. But SQL doesn't run them in that order. SQL runs them like this: first `FROM` (figure out which table). Then `WHERE` (filter the rows). Then `GROUP BY` if you have one. Then `HAVING` if you have one. Then `SELECT` (pick the columns). Then `ORDER BY` (sort). Then `LIMIT` (trim). Seven steps, in that exact order."
>
> "Why does this matter? Because it explains a bunch of things that otherwise look weird. For example — the column alias `AS total_orders` doesn't exist while WHERE is running, because WHERE runs before SELECT. So you can't write `WHERE total_orders > 100`; SQL would say 'I don't know what total_orders is yet'. We'll come back to this rule a few more times today, especially when we get to GROUP BY and HAVING. Tuck it in the back of your head: **FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT**. That's the runtime order."

### Q2 — How many were actually delivered?

> "Priya frowns when she sees 900. _'Wait. 900 orders, but how many actually got delivered? Some get cancelled, some refunded — I only care about the ones we made money on.'_"
>
> "Same query, just one more filter." [scroll to Q2]
>
> "Read it: `SELECT COUNT(*) AS delivered_orders FROM orders WHERE order_date = '2026-04-27' AND status = 'DELIVERED'`. We've added one new piece — `AND status = 'DELIVERED'`. Two filter conditions, joined together with `AND`."
>
> "Quick parking on `AND` and `OR`, because beginners trip on these all the time."
>
> "When you have multiple conditions in WHERE, you connect them with `AND` or `OR`. `AND` means **both must be true**. `OR` means **at least one must be true**. They're not interchangeable. If we'd written `OR` instead of `AND`, the query would have returned every delivered order ever, **plus** every order from yesterday regardless of status — way too many rows. So when in doubt, ask 'do I want both conditions met or just one?' and pick `AND` for both, `OR` for either. Your row count usually tells you immediately if you got it wrong; if it looks crazy high, check your AND-OR first."
>
> "One more nuance worth flagging. String comparisons in SQL are case-sensitive in many engines, including the one we're using. We wrote `'DELIVERED'` in uppercase because that's how the data is stored. If you wrote `'delivered'` in lowercase, you'd get zero rows back. Annoying gotcha, but normal. Match the casing of your data."
>
> [run the cell, wait 2 seconds]
>
> "About 797 delivered. So out of 900 orders yesterday, 797 actually made it to the customer. The rest got cancelled or refunded. That's roughly an 88% delivery rate — and that actually matches the simulator we built into the dataset. Good — the numbers make sense, which is always a sanity check you should do before reporting anything."

### Q3 — How much revenue yesterday?

> "Last question for Act 1. Priya wants the revenue. Money. How do we add up a column?"
>
> [scroll to Q3]
>
> "Two changes from query two. First — the `SELECT` clause. We don't use `COUNT` anymore. `COUNT` counts rows. We use `SUM(total_amount)` — `SUM` adds up the values in a numeric column. So instead of saying 'count me the rows', we're now saying 'add up the amounts for the rows that pass the filter'. Aggregate functions in SQL — `SUM`, `COUNT`, `AVG`, `MIN`, `MAX` — all work the same way: you give them a column, they collapse all the values across the rows into one number."
>
> "Second — exactly the same `WHERE` clause as query two. Same filter. We only want delivered orders from yesterday."
>
> [run the cell, wait 2 seconds]
>
> "₹574,000 and change. Priya nods. She has her three numbers. She walks away. Mission accomplished — we just wrote our first three SQL queries, and they were each three lines long."
>
> "Stop and notice what just happened. We learned `SELECT`, `FROM`, `WHERE`, `COUNT`, `SUM`, and the use of `AS` for aliases. Six pieces of SQL grammar in three queries. The shape was identical every time — pick what to show, pick the table, pick the filter. The only thing that changed was the function inside `SELECT`. Hold onto that pattern; we're about to add new pieces on top of it."
>
> [take a breath]

---

## [0:11 – 0:23] 🎬 Act 2 — Grouping and joins

**What we're learning:** how to combine two tables using `JOIN`, and how to collapse rows into groups using `GROUP BY`. This is the section where SQL stops feeling like a single-table tool and starts feeling like a real query language.

> "Priya comes back. _'I saw your numbers. But hang on — break it down by city. I want to know if Hyderabad is doing better than Bangalore. And while you're at it, tell me the top 5 restaurants this month.'_"
>
> "Two questions in this Act. They sound simple. They aren't — we need two new tools to answer them. First, we need a way to bring city information into our query, because city is **not** in the orders table. Second, we need a way to compute one number per city instead of one number for the whole company. Two new tools, both in this Act."

### Concept deep-dive — why we need a JOIN

> "Here's the problem we're facing." [scroll up briefly to show the orders table peek]
>
> "Look at the `orders` table. Each row has `customer_id`, `restaurant_id`, `total_amount`, `status` — but **no city column**. The city lives on the `restaurants` table — because city is a property of the restaurant, not of any individual order. So if we want to know 'how much revenue did Hyderabad make yesterday', we have to **bring two tables together**."
>
> "This operation is called a `JOIN`. The simplest mental model: **the tables hold hands by an ID column**. The `orders` table has a `restaurant_id`. The `restaurants` table also has a `restaurant_id`. They match up. When we say `JOIN restaurants ON o.restaurant_id = r.restaurant_id`, we're telling SQL 'glue these two tables together, row by row, wherever the IDs match'."
>
> "Picture it this way: imagine spreading both tables side by side. For each row in `orders`, SQL looks at the `restaurant_id`, walks over to the `restaurants` table, finds the row with the same ID, and zips them together into one wide row. Now that combined row has access to all the columns from both tables — order amount on one side, restaurant city and cuisine on the other. That's what JOIN does. It widens your data."

### Q4 — Revenue by city yesterday

> [scroll to Q4]
>
> "Let me read this slowly. `SELECT r.city, ROUND(SUM(o.total_amount), 2) AS revenue FROM orders o JOIN restaurants r ON o.restaurant_id = r.restaurant_id WHERE o.order_date = '2026-04-27' AND o.status = 'DELIVERED' GROUP BY r.city ORDER BY revenue DESC`."
>
> "That's a lot of new things in one query. Let me walk through it line by line, slowly, because there are at least four new concepts packed in here."
>
> "Line one: `SELECT r.city, ROUND(SUM(o.total_amount), 2) AS revenue`. We're selecting two things — the city, and the sum of revenue. The `r.` prefix says 'this column is from the restaurants table'. The `o.` prefix says 'this is from the orders table'. We need these prefixes once you've joined two tables, because SQL needs to know which one you mean. Otherwise it'll complain 'ambiguous column name'. The `ROUND(...)` function with the second argument 2 just rounds the SUM to 2 decimal places — that's pure cosmetic, makes the output look cleaner."
>
> "Line two: `FROM orders o`. Same as before, but with one new bit — `orders o`. The lowercase `o` after the table name is an **alias** for the table. Just shorthand. From here on we type `o.column` instead of `orders.column`. Saves keystrokes and reads cleaner. We saw column aliases in Act 1; this is the same idea, applied to tables."
>
> "Line three: `JOIN restaurants r ON o.restaurant_id = r.restaurant_id`. Same alias trick — `r` for `restaurants`. The `ON` clause is the matching rule. The two `restaurant_id` columns must equal. SQL uses this to glue rows together: for each order, find the matching restaurant row and combine them into one wider row."
>
> "Lines four and five: `WHERE o.order_date = '2026-04-27' AND o.status = 'DELIVERED'`. Same filter as Act 1. Note we're using `o.order_date` now because we've joined two tables; we have to be specific about which table we mean."
>
> "Line six: `GROUP BY r.city`. **This is the new mental model — the second big concept of this Act.** `GROUP BY` says: collapse all rows that have the same value in this column into a single output row. So all the orders from Hyderabad collapse into one row, all from Bangalore collapse into one row, and so on. We had thousands of orders coming out of the JOIN; we'll get 8 rows out of GROUP BY — one row per city, because there are 8 cities in our data."
>
> "But here's the obvious question — when you collapse 100 rows into one, what do you do with all the values? You can't keep them all. You have to decide. That's exactly what aggregate functions are for. The SELECT clause says 'give me the city, plus the SUM of the total_amount'. The city is the same for every row in the group, so it just appears once. The SUM adds up the amounts across all the rows in the group. That's the deal — every column in SELECT is either grouped or aggregated."
>
> "Line seven: `ORDER BY revenue DESC`. Sort the result with highest revenue first. `DESC` is short for 'descending'. Default is ascending if you don't specify."
>
> "One important rule about `GROUP BY` that trips up everyone the first time: **every column in your `SELECT` clause that isn't inside an aggregate function must also appear in the `GROUP BY` clause.** We have `r.city` in SELECT — so it must be in GROUP BY. We have `SUM(o.total_amount)` in SELECT — that's inside an aggregate, so it doesn't need to be in GROUP BY. If you forget this rule, SQL will throw an error like 'column not in GROUP BY'. Memorize the rule and you'll never see that error."
>
> [run the cell, wait 3 seconds]
>
> "There you go. Hyderabad on top, Bangalore second. Eight cities, eight rows, sorted by revenue. Priya can scan this in two seconds and see who's winning the day."

### Concept deep-dive — aliases and naming style

> "Quick tangent on aliases — those single letters `o` and `r` we used for the tables. Why bother with them?"
>
> "Two reasons. One, you save typing. In a query with three or four joined tables, `o.customer_id` is much faster to type than `orders.customer_id` repeated everywhere. Two, when you have a long table name like `delivery_assignments`, the alias `da` is just nicer to read."
>
> "There's a style debate in the SQL community. Some teams prefer no aliases — full table names, more readable to outsiders. Others prefer single-letter aliases — faster to type, more compact. My personal rule: if your query has more than two tables, use aliases. If it's one or two and the table names are short, full names are fine. Pick a style and be consistent within a single query — don't mix them halfway through."

### Q5 — Top 5 restaurants this month

> "Same shape as the previous query, but with three changes. Smaller groups, longer time window, and a hard limit on the output."
>
> [scroll to Q5]
>
> "Read it: `SELECT r.name, r.city, ROUND(SUM(o.total_amount), 2) AS revenue, COUNT(*) AS n_orders FROM orders o JOIN restaurants r ON o.restaurant_id = r.restaurant_id WHERE o.order_date >= '2026-04-01' AND o.status = 'DELIVERED' GROUP BY r.name, r.city ORDER BY revenue DESC LIMIT 5`."
>
> "Differences from the previous query — let me walk through them."
>
> "First, the SELECT has four columns now — name, city, revenue, and `COUNT(*)` for order count. Two aggregate columns side by side, no problem. SQL is happy to compute multiple aggregates in one pass over the data."
>
> "Second, `WHERE o.order_date >= '2026-04-01'`. Greater-than-or-equal-to. So 'this month' means any date from April 1 onwards. Combined with our data ending on April 27, that gives us April."
>
> "Third, `GROUP BY r.name, r.city`. We're grouping by two columns at once. Why both? Because two restaurants in different cities might happen to have the same name — like 'Truffles - Bangalore' and 'Truffles - Mumbai'. Grouping by name alone would merge them into one row, which would be wrong. Grouping by name plus city keeps them separate. Whenever you're grouping by something that might not be unique on its own, add another column to disambiguate."
>
> "Fourth, `LIMIT 5`. Take only the first five rows of the output. After ORDER BY DESC, the first five rows are the top five."
>
> "Common mistake here that I see all the time: people sometimes write `LIMIT 5` thinking it'll undo the ordering, or that it'll pick a random 5. It does neither. `LIMIT` runs absolutely last in the evaluation order — after SELECT, after ORDER BY. So you sort first, you limit last. The order matters. If you wrote `LIMIT 5` before `ORDER BY` in your query, SQL would still apply ORDER BY first internally — the keyword order in the query doesn't affect the runtime order, which is what we discussed earlier."
>
> [run the cell, wait 3 seconds]
>
> "And there are your superstars. The number-one restaurant in April is doing about ₹200,000 in revenue, on roughly 290 orders. That's the kind of insight Priya can take into a partner meeting and say 'these places are killing it — what are they doing right? Can we replicate that across other restaurants?'"
>
> [take a breath]
>
> "Quick recap of Act 2 before we move on. We learned `JOIN` — gluing two tables together by a shared ID. We learned `GROUP BY` — collapsing rows that share a value into one row. We learned table aliases — short names like `o` and `r`. And we learned the rule that every non-aggregate column in `SELECT` must appear in `GROUP BY`. Four big concepts. From here on, every advanced query you'll see is just stacking more of these on top of what we already have."

---

## [0:23 – 0:35] 🎬 Act 3 — Joins and finding what's missing

**What we're learning:** the difference between `INNER JOIN` and `LEFT JOIN`, and the powerful trick of using `LEFT JOIN` plus `IS NULL` to find missing data.

> "Marketing pings you in chat, not Priya this time. _'Hi, can we get a list of yesterday's orders — but with the customer name and restaurant name? IDs are useless to us. And while you're at it, can you pull a list of customers who haven't ordered in the last 30 days? We want to send them a discount push to win them back.'_"
>
> "Two requests in this Act. They sound similar. They are not — they need different kinds of joins. The first is an **inner** join. The second is a **left** join. The difference between these two is one of the most important ideas in SQL. It's worth getting right early, because every analyst spends their entire career picking between these two."

### Q6 — Names per order (INNER JOIN)

> "First request — names per order. Three tables involved here. `orders` is the spine, the data we're walking through. `customers` gives us the customer name. `restaurants` gives us the restaurant name. Three tables, two joins."
>
> [scroll to Q6]
>
> "Read it: `SELECT c.name AS customer, r.name AS restaurant, o.total_amount, o.status FROM orders o JOIN customers c ON o.customer_id = c.customer_id JOIN restaurants r ON o.restaurant_id = r.restaurant_id WHERE o.order_date = '2026-04-27' LIMIT 10`."
>
> "Two joins stacked on top of each other. Each one matches on a different ID column. The `orders` table has both `customer_id` and `restaurant_id`, so it can join out to both other tables. Notice the `AS customer` and `AS restaurant` aliases at the top — without them, both columns in the output would just be called `name`, and you couldn't tell which name was which. Aliases save you here."
>
> "Walking through it: `FROM orders o` — start with orders, alias `o`. `JOIN customers c ON o.customer_id = c.customer_id` — attach the customer record for each order. `JOIN restaurants r ON o.restaurant_id = r.restaurant_id` — attach the restaurant record. `WHERE o.order_date = '2026-04-27'` — filter to yesterday. `LIMIT 10` — show only the first 10 rows for sanity, since otherwise we'd dump 900 rows on screen."
>
> [run the cell, wait 3 seconds]
>
> "Beautiful. Marketing can read this. Names instead of cryptic IDs. Customer name on the left, restaurant name in the middle, amount and status on the right."
>
> "Now — what kind of join did we use here? It just says `JOIN`, but what SQL does by default is an **INNER JOIN**. That means: only rows where the match exists in **both** tables make it into the output. If an order had a `customer_id` that didn't exist in the customers table — orphan data — that order would silently disappear from the result. Inner join is strict. It only keeps matches. That's usually what you want, but not always — and the next query is exactly the case where it isn't."

### Concept deep-dive — INNER vs LEFT JOIN, and what NULL means

> "Let me draw this out in words, because this is the concept that separates beginners from intermediate analysts. Picture two tables side by side."
>
> "Imagine table A on the left and table B on the right. An **INNER JOIN** keeps only the rows where the keys match in both. The intersection. If A has 100 rows and B has 50 rows and only 30 of them match each other, you get 30 rows back. The other 70 from A and the other 20 from B are lost forever in the output."
>
> "A **LEFT JOIN** keeps every row from the left table, no matter what. For each left row, it tries to find a match on the right. If there's a match, you get the joined row with both sides populated. If there's no match, you still get the left row, but the right side is filled with `NULL` values. So if A has 100 rows and only 30 match B, a LEFT JOIN gives you all 100 rows back — 30 with real data on the right, 70 with NULLs on the right."
>
> "And **here's the trick** — if you want to find what's missing, customers with no orders, restaurants with no sales, products that never sold — you do a LEFT JOIN and then filter to where the right side is NULL. The NULLs are exactly the unmatched rows. That's how SQL expresses 'find me the absences'. There's no special FIND-MISSING keyword in SQL; you just LEFT JOIN and filter for NULL on the right."
>
> "Quick aside on NULL itself, because NULL behavior is weird and trips people up. NULL is **not** the same as zero. Zero is a real number. NULL means 'no value at all, unknown, missing'. Three things to remember about NULL. First, NULL doesn't equal anything — not even another NULL — so `WHERE col = NULL` doesn't work. You write `WHERE col IS NULL` instead. Second, NULL is ignored by aggregate functions like SUM and AVG, but `COUNT(*)` counts every row including NULLs while `COUNT(col)` only counts non-NULL values in that specific column. Third, NULL in arithmetic spreads — `5 + NULL` is NULL, not 5. NULL is contagious. Once you know these three rules, NULL stops surprising you."

### Q7 — Customers with no orders in last 30 days (LEFT JOIN)

> "Marketing's second request. Customers who haven't ordered in the last 30 days." [scroll to Q7]
>
> "Read it: `SELECT c.customer_id, c.name, c.city, MAX(o.order_date) AS last_order_date FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_date >= '2026-03-28' GROUP BY c.customer_id, c.name, c.city HAVING MAX(o.order_date) IS NULL LIMIT 15`."
>
> "Watch what's happening here, step by step. We start with **all** customers — that's `FROM customers c`. We left-join their orders, but only orders from March 28 onwards — the last 30 days. The date filter is **inside the JOIN's ON clause**, not in WHERE. That's important. Stay with me; I'll explain why in a second."
>
> "For each customer, we group by customer ID and look at the maximum order date across the joined rows. If the customer ordered any time in the last 30 days, that maximum is a real date — say March 30, or April 15. If they didn't order at all in the window, every joined row was NULL on the right side, so MAX returns NULL. That's our signal: NULL means 'this customer has been silent for 30 days'."
>
> "Then `HAVING MAX(o.order_date) IS NULL` filters to only the customers where the max is NULL — the silent ones. We used HAVING here, not WHERE, because MAX is an aggregate, and aggregates only exist after GROUP BY runs."
>
> "Now — the tricky part — why is the date filter inside the ON clause and not in WHERE? Because if you put `o.order_date >= '2026-03-28'` in WHERE, here's what happens. SQL evaluates the LEFT JOIN first, bringing in all customers including the silent ones with NULLs on the right. Then WHERE runs, and it throws away every row where order_date is NULL — which would throw away exactly the silent customers we're trying to find. The opposite of what we want. So we move the date filter into the ON clause, which means the join itself only matches recent orders, leaving the inactive customers with NULL on the right. They survive into the next step."
>
> "This is one of the trickiest things about LEFT JOIN, and worth saying again: **date filters or any conditions on the right-hand table belong in the ON clause, not in WHERE — at least when you're trying to preserve unmatched rows.** Got it? It's the kind of thing you'll get wrong once and then never forget."
>
> [run the cell, wait 3 seconds]
>
> "There's the marketing list. Every row says `last_order_date: None` — which is NULL — which means they didn't order in the window. Perfect re-engagement target. Marketing can take this list, send each customer a personalized 30%-off coupon, and try to win them back. This is exactly the kind of report that pays for an analyst's salary."

### Concept deep-dive — WHERE vs HAVING timing

> "One more concept to lock in before we move to Act 4. Did you notice we wrote `HAVING MAX(o.order_date) IS NULL` and not `WHERE MAX(o.order_date) IS NULL`? Let me say the rule explicitly, because it's going to come up again."
>
> "**WHERE runs before GROUP BY. HAVING runs after.** When you say `MAX(...)` or `COUNT(...)` or any aggregate, that aggregate doesn't exist until after the grouping happens. So you can't use it in WHERE — WHERE runs too early. You have to use HAVING."
>
> "The cheatsheet rule: WHERE filters rows before grouping. HAVING filters groups after grouping. WHERE is per-row. HAVING is per-group. If you want to filter on an aggregate value — SUM, COUNT, AVG, MAX, MIN — it's HAVING. If you want to filter on a raw column value, it's WHERE."
>
> "And remember the SQL evaluation order from Act 1: FROM, then WHERE, then GROUP BY, then HAVING, then SELECT, then ORDER BY, then LIMIT. WHERE happens before GROUP BY. HAVING happens after. Same data, but different filtering points. Once you internalize this, a lot of SQL stops feeling mysterious."
>
> [take a breath]

---

## [0:35 – 0:47] 🎬 Act 4 — CTEs and the silent churners problem

**What we're learning:** Common Table Expressions, written with the `WITH` clause. This is the section that turns SQL from "writing single queries" into "writing readable, multi-step analysis". It's the highest-value concept in this hour.

> "Priya's back. She's been thinking. _'Look — I want to know who our **silent churners** are. People who used to be active, who suddenly stopped. Not new customers, not occasional ones — actual lost customers we should win back.'_"
>
> "This is a real business question. The most valuable kind, because the answer is directly actionable. It's also our hardest one yet from a SQL perspective. So let me define silent churner very slowly, because the definition is the entire game."
>
> "A **silent churner** is somebody who placed at least 8 delivered orders in January and February — so they were a real, regular customer, not just a casual one — and then placed zero orders in March and April. They didn't slow down. They didn't drift off. They left."
>
> [pause]
>
> "Now — think about how you'd actually answer that question with a pen and paper. You'd make two lists. **List A**: customers who were active in January and February, with at least 8 orders. **List B**: customers who placed any orders in March or April. The answer is: everyone in list A who is **not** in list B. **List one minus list two.**"
>
> "I'm going to repeat that phrase a few times during this Act, because it's the framing for the whole query: **list one minus list two**."

### Concept deep-dive — why CTEs are readable, not advanced

> "If you tried to write 'list one minus list two' as one giant SQL query, it would be unreadable. You'd have subqueries inside subqueries inside subqueries, three or four levels deep. You'd come back to it next week and have no idea what it does. So SQL gives us a tool that lets you write the steps in order, with names. It's called a **CTE — Common Table Expression** — or just `WITH` for short."
>
> "I want you to forget the rumor that CTEs are 'advanced'. They are not. They are the **opposite** — they're the tool that makes hard queries **readable**. You break the question into named sub-questions. You define each one with a name. And then you use those names in your final query as if they were tables."
>
> "Mental model: a CTE is a temporary result set that exists only for the duration of one query. Like a variable in any normal programming language, but in SQL. You define it at the top of your query with `WITH name AS (...)`, and then you can refer to `name` later as if it were a real table. SQL throws it away when the query finishes — it doesn't persist anywhere."
>
> "The syntax shape is: `WITH first_step AS (some query), second_step AS (another query that maybe uses first_step) SELECT ... FROM second_step`. Two CTEs separated by a comma — note the comma between them, no `WITH` keyword on the second one. Then the final SELECT at the bottom. You can have as many CTEs as you need; some real-world queries have six or seven CTEs stacked up."
>
> "And the readability win is enormous. When somebody comes back to read your query in three months — or worse, when **you** come back to read your own query in three months — they can read each CTE in order: first this, then that, then the final answer. Each step has a name. The logic is visible. No untangling needed."
>
> "Hold the phrase in your head: list one minus list two. That's the shape of the query coming up."

### Q8 — Silent churners

> "Look at Q8. Don't read the SQL line by line yet — read the **structure** first. There's a `WITH active_in_jan_feb AS (...)`, then a comma, then `active_in_mar_apr AS (...)`, then the final `SELECT` at the bottom. Three sections. Three named steps. List A, list B, and the combination."
>
> [scroll to Q8]
>
> "Now we go through each piece slowly. This is the longest query in the session, but it's not actually complicated — it's three small queries glued together with names."
>
> "**Step one**, named `active_in_jan_feb`. The query inside the parentheses says: `SELECT customer_id, COUNT(*) AS orders_jan_feb FROM orders WHERE order_date BETWEEN '2026-01-01' AND '2026-02-28' AND status = 'DELIVERED' GROUP BY customer_id HAVING COUNT(*) >= 8`. In English: from the orders table, look at delivered orders between January 1 and February 28, group by customer, count their orders, keep only customers with at least 8 orders. That's list A — regulars from Jan-Feb."
>
> "Quick note on `BETWEEN ... AND ...` — it's inclusive on both sides. So `BETWEEN '2026-01-01' AND '2026-02-28'` includes both January 1 and February 28. Same as writing `>= '2026-01-01' AND <= '2026-02-28'`, just shorter."
>
> "Note also we used `HAVING COUNT(*) >= 8` and not `WHERE COUNT(*) >= 8`. Why? Because — and we've seen this rule twice now — WHERE runs before GROUP BY, HAVING runs after. The COUNT doesn't exist until after grouping, so we can only filter on it with HAVING. Same rule from Act 3, applied again here."
>
> "**Step two**, named `active_in_mar_apr`. Simpler query: `SELECT DISTINCT customer_id FROM orders WHERE order_date BETWEEN '2026-03-01' AND '2026-04-27' AND status = 'DELIVERED'`. Just give me the list of customer IDs who placed any delivered order in March or April. `DISTINCT` removes duplicates so each customer appears only once in the list. That's list B."
>
> "Now the **final step** — the actual SELECT at the bottom of the query. `SELECT c.customer_id, c.name, c.city, a.orders_jan_feb FROM active_in_jan_feb a JOIN customers c ON a.customer_id = c.customer_id WHERE a.customer_id NOT IN (SELECT customer_id FROM active_in_mar_apr) ORDER BY a.orders_jan_feb DESC LIMIT 20`."
>
> "Read it as: take list A — the regulars from Jan-Feb, aliased as `a`. Join to the customers table to get names and cities. Filter to only the customers whose ID is **NOT IN** list B — the people who didn't order in Mar-Apr. Order by how active they were in Jan-Feb, most active first. Top 20."
>
> "The `NOT IN` is the magic of this query. It's a sub-query that says 'don't include any customer ID that appears in this other list'. That's our 'list A minus list B' operation, expressed in SQL. The whole CTE structure exists so this final NOT IN sub-query can have a clean, readable name to refer to. Without CTEs, you'd have to inline the entire active_in_mar_apr query inside the NOT IN parentheses, and the final query would be five times harder to read."
>
> [run the cell, wait 5 seconds]
>
> "And there's the result. About 1,150 silent churners total in our data — people who were ordering 15, 16, even 17 times in two months and then completely disappeared in March-April. **Real churn.** This is gold for the retention team. They can take this list, segment it by city, send each customer a personalized 30%-off coupon, and try to win them back. This kind of query is the difference between an analyst who reports numbers and an analyst who drives revenue."

### Why this matters

> "Pause for a second. Look at what we just did. We answered a real, valuable business question — who are our silent churners? — by breaking it into two named sub-questions and combining them with a NOT IN. **List one minus list two.** That's the entire pattern for senior analyst work."
>
> "Most analysis questions look like this. 'Something minus something.' 'Compare A to B.' 'Find the difference between this and that.' 'Customers who do X but not Y.' 'Products that sell well in March but not in April.' CTEs let you write each part as a clearly-named step, so anyone reading your query — including you, three months later — understands the logic immediately. That's the readability point I keep coming back to."
>
> "If you take **one** thing away from this hour, take this: don't be afraid of CTEs. They are not advanced. They are the tool that makes everything after them easier. The list-one-minus-list-two pattern alone will solve a third of the questions you'll face as an analyst."
>
> [take a breath]

---

## [0:47 – 0:55] 🎬 Act 5 — Window functions and CASE WHEN

**What we're learning:** how to rank within groups using window functions, and how to bucket continuous values into named categories using CASE WHEN.

> "Last act. Priya comes back one final time. _'What's the top cuisine in **each** city this month? I want one row per city, with the cuisine that's earning the most. Different city, different cuisine — show me which one is winning where.'_"
>
> "Sounds simple. But there's a catch. If you `GROUP BY city, cuisine` and `ORDER BY revenue DESC`, you get the top cuisine **overall** — not the top cuisine per city. Because GROUP BY collapses, and once it collapses, you can't say 'top one within each group' anymore. You'd just see the overall winner."

### Concept deep-dive — PARTITION BY vs GROUP BY

> "We need a new tool. A **window function**. The mental model is one phrase, please commit it to memory:"
>
> "**`PARTITION BY city` means: do this calculation separately for each city, but don't merge the rows.**"
>
> "That's the difference from GROUP BY. GROUP BY collapses 100 rows into 8 rows — one row per group. PARTITION BY keeps the 100 rows but adds a column that tells you the rank, or the running total, or whatever you computed, within each group. Same input, different output shape. PARTITION BY preserves rows; GROUP BY collapses them. That is the entire concept."
>
> "The most common window function is `ROW_NUMBER()` — it numbers the rows from 1 upwards within each partition, ordered by whatever you specify. Sister functions are `RANK()` (where ties share rank, with gaps after) and `DENSE_RANK()` (where ties share rank, no gaps). For top-N-per-group queries like this one, `ROW_NUMBER()` is what you usually want — it always gives unique ranks, even when there are ties. There are also `LAG()` and `LEAD()` for peeking at the previous or next row, and `SUM() OVER (...)` for running totals. They all share the same `OVER (PARTITION BY ... ORDER BY ...)` syntax."

### Q9 — Top cuisine per city this month

> "Look at Q9. Two CTEs and a final select. We're using CTEs again because the structure is naturally two-step." [scroll to Q9]
>
> "First CTE — `cuisine_revenue` — computes the revenue for each city-cuisine pair this month. Standard GROUP BY query, nothing new there. We have one row per (city, cuisine) combination, with the total revenue."
>
> "Second CTE — `ranked` — takes that result and adds a column: `ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) AS rk`. Read that whole expression in English: 'number these rows from 1 upwards, **separately for each city**, ordered by revenue descending'. The Biryani row in Hyderabad gets rank 1 if Biryani is the top earner in Hyderabad. The Pizza row in Pune gets rank 1 if Pizza wins Pune. Eight cities, eight rank-1 rows, one per city."
>
> "Then the final select keeps only the rows where `rk = 1` — the top cuisine in each city. Eight cities, eight winners."
>
> "Line by line on the window function syntax: the function name is `ROW_NUMBER()`. The `OVER` keyword starts the window definition. Inside the parentheses: `PARTITION BY city` — split the data into groups by city, but don't collapse them. `ORDER BY revenue DESC` — within each partition, order the rows by revenue, highest first. `AS rk` — name the output column 'rk' for shorthand."
>
> "Common mistake one: forgetting the `OVER` keyword. `ROW_NUMBER()` by itself doesn't do anything; you need `OVER (...)` to tell it how to partition and order. Common mistake two: putting the `ORDER BY` outside the OVER parentheses. The ORDER BY inside `OVER` is for the window — it controls how rows are numbered within each partition. The ORDER BY at the end of the entire query is for the final output sort. They're different things, and they can both exist in the same query, doing different jobs."
>
> [run the cell, wait 3 seconds]
>
> "Beautiful. Different city, different cuisine. Hyderabad has its top cuisine. Bangalore has its top cuisine. Mumbai has its top cuisine. Pune has its top cuisine. Each city has its own personality, and we can see it all in one query. This kind of breakdown is exactly the kind of thing a regional manager wants on a dashboard."
>
> "This is the bridge to senior analyst work. Once you have window functions in your toolkit, you can answer 'top N per group', 'compare each row to the previous row using LAG', 'running totals using SUM OVER', 'percentile rankings'. All the things that tell stories instead of just totals."

### Bonus — CASE WHEN

> "One bonus pattern before we close out. CASE WHEN. This is the SQL equivalent of if-elif-else from any normal programming language."
>
> "Sometimes you want to bucket continuous values into named groups. Like converting `rating_avg` (which is a number from 3.0 to 4.9) into '4.5+ stars' / '4.0 to 4.4 stars' / and so on. That's exactly what CASE WHEN does."
>
> [scroll to bonus query]
>
> "The shape is: `CASE WHEN condition1 THEN value1 WHEN condition2 THEN value2 ELSE default_value END AS column_name`. Each WHEN is a condition, evaluated top to bottom. The first WHEN that matches wins. ELSE catches everything not matched by any WHEN. The whole thing is wrapped in `CASE ... END` and aliased like any other column."
>
> "In our query: WHEN rating_avg >= 4.5 THEN '4.5+ stars'. WHEN rating_avg >= 4.0 THEN '4.0-4.4 stars'. And so on. The order matters — if a restaurant has rating 4.7, the first condition matches, so it gets '4.5+ stars'. SQL doesn't keep checking; it stops at the first match. So always order your CASE conditions from most specific or highest to least specific or lowest, otherwise everything could fall into the first bucket."
>
> [run the cell, wait 3 seconds]
>
> "And we get a clean breakdown: how many restaurants in each rating bucket, how much revenue each bucket pulled in. CASE WHEN works inside SELECT (like here, creating a new column), inside WHERE (filtering), inside GROUP BY (grouping by a derived value), inside ORDER BY. Anywhere a value or expression is allowed in SQL, CASE WHEN works."
>
> [take a breath]

---

## [0:55 – 1:00] Closing recap and Q&A

> "Five minutes left. Let me close the loop, then take questions."

### The 9 concepts

> "We covered nine SQL concepts in the last 50 minutes. Let me read them back so they stick."
>
> "**One.** SELECT and FROM — pick columns from a table. **Two.** WHERE — filter rows before any grouping. **Three.** COUNT, SUM, AVG, the aggregate functions. **Four.** GROUP BY — collapse rows that share a value into a single row. **Five.** ORDER BY and LIMIT — sort and trim the output. **Six.** INNER JOIN — combine two tables on a shared key, keeping only matches. **Seven.** LEFT JOIN — keep all rows from the left table, with NULLs on the right when there's no match, and use IS NULL to find absences. **Eight.** Common Table Expressions, the WITH clause — break a query into named, readable steps. **Nine.** Window functions, OVER PARTITION BY — rank or compare within groups, without collapsing rows."
>
> "Plus a bonus concept: CASE WHEN, for bucketing continuous values into named categories."
>
> "If two weeks from now you can look at a table and ask any of these nine kinds of questions in your head, you are functioning as a data analyst. The rest is just experience and practice."

### The closing line

> "One thing to walk away with. Repeat in your head:"
>
> "**SQL isn't a language you memorise. It's a way of asking questions of a table.** Every query you'll ever write is some combination of: which columns do I want, which table do I query, what filter applies, grouped by what, joined to what else. That's the whole shape. The more questions you ask of real data, the more fluent you get."
>
> "The repo link is in the chat — bookmark it now if you haven't. The notebook we just walked through is in there, fully runnable on Colab. There are 20 graded practice exercises with full solutions. There's a one-page cheatsheet. There's a `run_locally.md` if you'd rather use DBeaver or PostgreSQL at your desk instead of Colab."

### Pre-written answers for the four questions you'll get

> "Now — five minutes for questions. While people unmute or type in chat, let me pre-empt the four questions I always get at the end of these sessions, because they save us time."

**On SQL dialects:**

> "First: 'What's the difference between SQL dialects — SQLite, PostgreSQL, MySQL, BigQuery, Snowflake?' Answer: ninety percent of what we covered today is identical across all of them. Window functions are universal. Joins are universal. CTEs are universal. The dialect differences are concentrated in date functions, string functions, and a few advanced features. So `julianday` in SQLite becomes `date_trunc` in PostgreSQL becomes `DATE_DIFF` in BigQuery. JSON handling differs. Specific data types differ. When you switch dialects, you'll spend an afternoon learning the differences, not a week. The core grammar — SELECT, FROM, WHERE, JOIN, GROUP BY, HAVING, ORDER BY, WITH — is exactly the same everywhere."

**On Pandas:**

> "Second: 'How is this different from Pandas? I already know Pandas.' Answer: Pandas runs in your laptop's memory, in a single Python process, on data that fits in RAM. SQL runs on a database server, possibly distributed across many machines, on data that does not fit in memory. For datasets under a few gigabytes, they're roughly interchangeable — same operations, different syntax, pick the one your team uses. For datasets over that, SQL is the only realistic option. Also: Pandas is great for ad-hoc analysis where you control everything; SQL is better for production data pipelines, scheduled jobs, and team collaboration where the data lives in a shared place. Most professional analysts end up using both daily."

**On NoSQL:**

> "Third: 'Should I learn NoSQL too?' Answer: yes, eventually, but not yet. NoSQL is a different shape of database for a different shape of data. SQL is for structured tabular data with relationships — what most business analytics looks like. NoSQL covers documents (MongoDB), key-value stores (Redis), graphs (Neo4j), or massive append-only event logs (Cassandra). You'd usually pick the database first based on your data shape, then learn its query language. For now, SQL is your highest-leverage skill. Add NoSQL later when you have a specific use case that needs it."

**On where to practice:**

> "Fourth: 'Where do I practice more after this session?' Answer: three places. First, the 20 exercises in the repo I just shared in chat — they're graded beginner to advanced, with full solutions for each. Second, leetcode dot com slash problemset slash database — about 200 SQL problems sorted by difficulty, with discussion threads where people compare approaches. Third, and most important, your own work data. Pick a question you're actually curious about at your job, write the SQL, double-check the answer manually for a sample of rows. The faster you ask real questions of real data you care about, the faster you become fluent. There's no substitute for that."
>
> "Okay — four minutes left. Open chat. Any questions in the next four minutes, I'll take them. Anything I miss, drop it in chat after we end and I'll respond by email. Watch chat now."
>
> [Q&A — take 1-2 questions if any arrive, otherwise wrap]
>
> "Thanks everyone. The repo link is in the chat. Good luck with the SQL — and the next time someone walks up to your desk and asks 'how did we do yesterday', you'll know exactly what to type."

---

# Speaker tips appendix (online screen-share specific)

## If the audience seems quiet or unresponsive

- They will. They're muted, they're watching, you have no feedback channel during the session. This is normal. Don't get rattled.
- Trust the script. Trust that the explanation is landing. They're listening.

## If you're 5 minutes behind schedule

- The fastest cuts: drop the bonus CASE WHEN section entirely (8 minutes back), and the SQL dialects pre-written answer in the Q&A. That's about 10 minutes recovered.
- Do not skip Q8 (CTEs). It's the highest-value query of the hour. People came for that one even if they don't know it.
- Do not skip the 9-concept recap at the end. Audiences need it for closure.

## If a query you run on screen returns an unexpected result

- Acknowledge briefly: "Hmm, that's not what I expected — let me check." Then check it. If it's a data quirk, say so and move on. If it's a typo, fix it and re-run.
- Never bluff. If 30 people are watching your screen, they'll notice. Calm acknowledgment beats hidden panic every time.

## If your screen-share crashes mid-session

- Stay calm. Announce: "I've lost screen-share, give me 20 seconds to restart it." Then restart. Don't apologize repeatedly.
- The notebook is still loaded in your browser. Once screen-share is back, you're exactly where you left off.

## Energy management for long online delivery

- Online speaking is more tiring than in-person because you don't get the energy back from the room. Drink water at every Act break, even if you don't feel thirsty.
- The two natural energy dips for the audience are around minute 12 (mid-Act 2) and minute 45 (mid-Act 4). Pick up your tone slightly during those windows.
- Don't apologize for technical issues — just solve them. Audiences are very forgiving online if you stay calm.

## If you finish 3 minutes early

- Don't pad. Just say: "We finished a few minutes early. Take the extra time, dig into the practice exercises in the repo, and message me with any questions." Then end the call.
- Going long online is much worse than ending early. People appreciate getting their time back.
