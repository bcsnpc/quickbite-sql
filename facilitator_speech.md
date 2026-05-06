# Facilitator speech — QuickBite SQL session

A 60-minute spoken script. Read it once before the session, then keep it open in a side window so you can glance during transitions. Lines in `[brackets]` are stage directions, not spoken. Lines marked **(BACKUP)** are slow re-explanations to use only if the room looks lost.

---

## Pre-session checklist (do this 10 minutes before)

1. Open the Colab notebook in **your** browser, run the setup cell, confirm it works on the projector.
2. Open the GitHub repo in a second tab — you'll need to point people to `cheatsheet.md` and the exercises folder.
3. Have `notebook/QuickBite_SQL_Story.ipynb` zoomed at ~125% so the back row can read it.
4. Test the projector colour: SQL syntax highlighting needs to be visible. If reds/greens are washed out, switch to a high-contrast theme.
5. Have water nearby. You'll be talking continuously for 50 of the next 60 minutes.

---

## [0:00 – 0:05] Welcome and setup

> "Hi everyone, welcome. Before we start — please open this link on your laptop." [show the Colab link on screen]
>
> "While that's loading, a quick question: by show of hands, who has written a `SELECT` statement before, even once? … Okay, and who's never opened a SQL editor in their life? … Good, mixed group. That's exactly the room I planned for."
>
> "Here's what we're going to do for the next 60 minutes. You're a new data analyst at a food delivery company called QuickBite. We work in 8 Indian cities. The CEO — her name is Priya — is going to walk up to your desk and ask you 9 questions over the next hour. Each question is going to force you to learn one new piece of SQL. By the time we're done, you will have used `SELECT`, `WHERE`, `JOIN`, `GROUP BY`, CTEs, and window functions. Nine concepts in nine queries."
>
> "Now run the first cell — the one with `pip install` at the top. It's going to take about 30 seconds to download the data. While it runs, look at the table on the very first markdown cell — `customers`, `restaurants`, `orders`, and so on. Get a feel for the column names. We'll come back to it."
>
> [pause ~30 seconds — walk around, check screens]
>
> "Everyone got the green tick? `Ready` message? Good. If your setup cell failed — usually it's a network thing — try once more. If it still fails, partner up with your neighbour. Don't lose 10 minutes debugging Colab; that's not why we're here."

---

## [0:05 – 0:15] 🎬 Act 1 — Simple questions (Q1, Q2, Q3)

> "Okay, scene one. It's Tuesday morning. You're at your desk. You've barely opened your laptop. Priya walks up — coffee in hand — and says, _'Quick one. How did we do yesterday? Just give me the numbers.'_"
>
> "Right. So Priya wants to know about yesterday — which in our story is **2026-04-27**. She wants three things: how many orders, how many actually got delivered, and how much revenue."
>
> "Let me show you SQL's biggest secret — and I'm not joking, this is the entire mental model. **SQL is just a way of asking questions of a table.** That's it. The grammar is a little different, but you're really just saying 'show me X from Y where Z'."

### Q1 — Total orders yesterday

> "First question Priya asked: how many orders. Look at this query." [show Q1 cell]
>
> "Read it like English: `SELECT COUNT of all rows FROM the orders table WHERE the order_date is yesterday`. Three lines. Three ideas: what to show, where to look, how to filter."
>
> "`SELECT COUNT(*)` — `COUNT(*)` means count every row. The star means 'every row'."
> "`FROM orders` — that's the table."
> "`WHERE order_date = '2026-04-27'` — that's our filter for yesterday."
>
> "Hit run." [run cell]
>
> "There you go. 900 orders. Priya is happy."

### Q2 — Delivered yesterday

> "Now Priya frowns. _'Wait. 900 orders, but how many actually got delivered? Some get cancelled, some refunded — I only care about the ones we made money on.'_"
>
> "Same query, just one extra filter. Look at this — we add `AND status = 'DELIVERED'`. That's it." [show Q2]
>
> "When you have multiple conditions in `WHERE`, you connect them with `AND`. Or `OR`. There's no special trick."
>
> [run Q2] "About 797. So out of 900 orders, 797 made it. Roughly 88% delivery rate, which actually matches what the data team built into the simulator."

### Q3 — Revenue yesterday

> "Last question for Act 1. Priya wants the revenue. Money. How do we add up a column?"
>
> "We don't use `COUNT` — `COUNT` counts rows. We use `SUM` — sum adds up values in a column." [show Q3]
>
> "`SELECT SUM(total_amount)`. That's it. Same `WHERE` clause as Q2."
>
> [run Q3] "₹574,000-something. Priya nods, takes her coffee, walks away. You feel pretty good."

### Audience check + try-this

> "Pause. Everybody with me? You've now seen `SELECT`, `WHERE`, `COUNT`, `SUM`. That's three concepts in 5 minutes. Nothing fancy yet — but if you can tweak these three queries, you're already useful."
>
> "Look at the **try this** box. Three small variations — count cancellations, query a different date, get the average. Take one minute, modify one of the queries above and run it. I'll come around."
>
> [pause for ~60 seconds, walk the room, answer questions one-on-one]

**(BACKUP if anyone is still confused)**: "Look at the screen. The query has three parts. The top says what to show. The middle says where to look. The bottom says what to filter. That's the entire pattern. We're going to use that same shape for the rest of the session — just adding more pieces on top."

---

## [0:15 – 0:27] 🎬 Act 2 — Grouping (Q4, Q5)

> "Okay, Act 2. Priya comes back. _'I saw your numbers. But hang on — break it down by city. I want to know if Hyderabad is doing better than Bangalore. And by the way, who are the top 5 restaurants this month?'_"
>
> "She's asking for the same kind of data — counts and sums — but **per city**, not as one big total. This needs a new tool: `GROUP BY`."

### Q4 — Revenue by city yesterday

> "But before we get to `GROUP BY`, there's a problem. Look at the `orders` table. There's no city column. The city lives on the `restaurants` table. So we have to **bring two tables together**."
>
> "This is called a `JOIN`. The simplest way to think about it: **the tables hold hands by an `id` column**." [hold hands gesture if you're a hand-talker]
>
> "`orders` has a `restaurant_id`. `restaurants` has a `restaurant_id`. They match up on that column. When we say `JOIN restaurants ON o.restaurant_id = r.restaurant_id`, we're saying 'glue these two tables together wherever the IDs match'."
>
> [show Q4] "Look at the query. We've added two things: the JOIN line that glues the tables, and the `GROUP BY r.city` line at the bottom. Then we sum the revenue."
>
> "Read it like English: take orders, attach each order to its restaurant so we know the city, keep only delivered orders from yesterday, then **collapse all the rows that share the same city** into one row, sum the revenue, and sort highest first."
>
> "That's the entire mental model for `GROUP BY`. **Collapse rows that share a value into one row, then aggregate the rest.**"
>
> [run Q4] "There you go. Hyderabad on top, Bangalore second. Priya can see at a glance which city is performing."

### Q5 — Top 5 restaurants this month

> "Q5 is the same shape, but smaller groups. Instead of grouping by city, we group by restaurant. Instead of one row per city, one row per restaurant."
>
> [show Q5] "Same JOIN, same GROUP BY pattern — except we group by `r.name, r.city`. We add a `LIMIT 5` at the end so we only see the top 5."
>
> [run Q5] "And there are your superstars. The number-one restaurant is doing about ₹200,000 in April."

### Audience check + try-this

> "Quick check — does `GROUP BY` make sense? It's just 'collapse the rows that share this value, aggregate the rest'. If your `SELECT` has `r.city`, then `GROUP BY r.city`. If your `SELECT` has `r.name, r.city`, then `GROUP BY r.name, r.city`. The columns have to match."
>
> "Mini-exercise time. Look at the **try this** cell. Try grouping by cuisine instead of city. Or by payment method. Don't write from scratch — copy Q4 and just change the column."
>
> [pause ~90 seconds]

**(BACKUP — if half the room looks lost)**: "Let me say that again differently. Imagine you have a stack of order receipts on your desk. You want one number per city. So you sort the stack into 8 piles — one pile per city. Then for each pile, you add up the amounts. Eight cities, eight piles, eight sums. That's `GROUP BY city`. The `JOIN` was just because the receipts didn't have the city written on them — we had to look up the restaurant first."

---

## [0:27 – 0:40] 🎬 Act 3 — Joins (Q6, Q7)

> "Act 3. The marketing team comes over now, not Priya. _'Hi, can we get a list of yesterday's orders — but with the customer name and restaurant name? IDs are useless to us. And — also — we want to send a discount push to people who've gone silent in the last month. Can you pull that?'_"
>
> "Two requests. They sound similar. They're not. The first is an **inner join**. The second is a **left join**. And the difference between these two is one of the most important ideas in SQL."

### Q6 — Names per order (INNER JOIN)

> "First request — names per order. We've got `orders` (the spine), `customers` (gives us the customer name), and `restaurants` (gives us the restaurant name). Three tables, two joins."
>
> [show Q6] "Read it: from orders, join customers on customer_id, join restaurants on restaurant_id, filter to yesterday, show the customer name, the restaurant name, the amount, the status."
>
> [run Q6] "Beautiful. Marketing can read this. Names instead of cryptic IDs."
>
> "Now — what kind of join did we use here? It says just `JOIN`, but what SQL does is an **INNER JOIN** by default. That means: only rows where the match exists in **both** tables. If an order had a customer_id that doesn't exist in the customers table, that order would just disappear from the result. Inner join is strict."

### The hand demo for INNER vs LEFT JOIN

> "I want to show you the difference between `INNER JOIN` and `LEFT JOIN` physically. Watch my hands."
>
> "Imagine my left hand is the customers table. My right hand is the orders table. **An INNER JOIN** —" [hold hands together with all fingers touching, showing intersection] "— only keeps the rows that match on both sides. If a customer has no orders, they don't show up."
>
> "**A LEFT JOIN** —" [keep left hand fully open, only the matching part of the right hand connects] "— keeps every row from the **left** table no matter what. If there's no match on the right, you just get `NULL`s on the right side."
>
> "And **the trick is**: if you want to find absences — customers with no orders, restaurants that never sold anything, products that never sold — you `LEFT JOIN` and then filter to where the right side is `NULL`. That's how you find what's missing."

### Q7 — Customers with no orders in last 30 days (LEFT JOIN)

> "Marketing's second request. Customers who haven't ordered in the last 30 days." [show Q7]
>
> "Watch what happens. We start with **all** customers. We left-join their orders, but only orders from the last 30 days. Then for each customer, we check the maximum order_date. If they had any orders in the window, that maximum is a date. **If they had no orders at all, the maximum is `NULL`** — because every joined row was `NULL` on the right side."
>
> [run Q7] "There's the marketing list. Every row says `last_order_date: None` — which is `NULL` — which means they didn't order in the window. Perfect re-engagement target."

### WHERE vs HAVING

> "One more thing in Act 3. Did anybody notice we wrote `HAVING MAX(o.order_date) IS NULL` and not `WHERE MAX(o.order_date) IS NULL`? Why?"
>
> "**`WHERE` runs before `GROUP BY`. `HAVING` runs after.** When you say `MAX(...)`, that's an aggregate — it doesn't exist until after the grouping happens. So you can't use it in `WHERE`; you have to use `HAVING`."
>
> "Cheat sheet for life: `WHERE` filters rows, `HAVING` filters groups. That's the timing rule."
>
> [pause for questions]

### Try-this

> "Three exercises in the try-this box. The third one is the find-absence pattern in disguise — restaurants that have never received an order. Try that one. Tells you who's not earning their place on the platform."

---

## [0:40 – 0:52] 🎬 Act 4 — CTEs (Q8) — the highest-risk section

> "Act 4. Priya's back. She has been thinking. _'Look — I want to know who our **silent churners** are. People who used to be active. People who suddenly stopped. Not new customers, not occasional ones — actual lost customers we should win back.'_"
>
> "This is a real business question. It's also our hardest one yet. Let me define **silent churner** very slowly, because the definition is the whole game."
>
> "A **silent churner** is somebody who was placing **at least 8 orders during January and February** — so a real, regular customer — and then has placed **zero orders** in March and April. They didn't slow down. They didn't go quiet. They left."
>
> "[pause and watch the room]"
>
> "Think about how you'd actually answer that question with a pen and paper. You'd make two lists. **List A**: customers who were active January-February. **List B**: customers who placed any orders March-April. The answer is everyone in A who is not in B. **List one minus list two.**"

### Why we need CTEs

> "Now if you tried to write that as one giant query, it would be unreadable. Sub-queries inside sub-queries. So SQL gives us a tool that just lets you write the steps in order, with names. It's called a **CTE — Common Table Expression** — or just `WITH`."
>
> "I want you to forget that CTEs are sometimes called 'advanced'. They're not advanced. They're the **opposite** — they're the tool that makes hard queries **readable**. You define each step, give it a name, and then use that name later."

### Q8 — read the English first, the SQL second

> "Look at this query. **Don't read the SQL yet.** Read the structure: there's a `WITH active_in_jan_feb AS (...)`, then a comma, then `active_in_mar_apr AS (...)`, then the final `SELECT`. Three sections. Three named steps."
>
> [show Q8]
>
> "Step 1, `active_in_jan_feb` — find customers with at least 8 delivered orders in Jan-Feb. That's list A."
>
> "Step 2, `active_in_mar_apr` — find customers who placed any delivered order in Mar-Apr. That's list B."
>
> "Final step — give me everyone in list A whose `customer_id` is `NOT IN` list B. With their name and city. Sorted by how active they were."
>
> "That's it. Three steps in English, three steps in SQL. Run it."
>
> [run Q8] "You see the result. About 1,150 silent churners — people who were ordering 15-17 times in two months and then disappeared. **Real churn.** This is gold for the retention team."
>
> [pause]

**(BACKUP — 30-second simplified explanation if the room is lost)**: "Forget the syntax for a second. Imagine you have two whiteboards. On the first whiteboard you write down everyone who ordered a lot in Jan-Feb. On the second whiteboard you write down everyone who ordered anything in Mar-Apr. Now you take whiteboard one, and you cross out anyone whose name also appears on whiteboard two. What's left on whiteboard one is your churn list. The `WITH` clause is just a way of telling SQL 'these are my whiteboards, here's what's on each one'."

### Try-this

> "Pause. Sip water. This was the hardest concept in the session. From here on, it's mostly variations on what you've already seen."
>
> [pause for questions — give this 90 seconds, it's the section where people most often have them]

---

## [0:52 – 1:00] 🎬 Act 5 — Window functions + closing

> "Last act. Priya comes back one final time. _'What's the top cuisine in **each** city this month? I want one row per city, with the cuisine that's earning the most.'_"
>
> "Sounds simple. But there's a catch. If you `GROUP BY city, cuisine` and `ORDER BY revenue DESC`, you get **the top cuisine overall** — not the top per city. Because `GROUP BY` collapses; it doesn't rank within groups."
>
> "So we need a new tool: a **window function**. The mental model is one phrase, please commit it to memory: **`PARTITION BY city` means 'do this calculation separately for each city, but don't merge the rows.'**"
>
> "That's the difference from `GROUP BY`. `GROUP BY` collapses 100 rows into 8 rows. `PARTITION BY` keeps the 100 rows but adds a column that tells you the rank within each group."

### Q9 — top cuisine per city

> [show Q9] "Two CTEs again. First, cuisine_revenue — the revenue per (city, cuisine) pair. Second, ranked — same data but with `ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC)`. Then the final select keeps only the rows where the rank is 1."
>
> "Read the window function out loud — `ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC)`. In English: 'number these rows from 1 upwards, **separately for each city**, ordered by revenue descending.' One sentence."
>
> [run Q9] "Beautiful. Different city, different cuisine. Hyderabad → Biryani, no surprise. Bangalore → Continental. Mumbai → North Indian. Pune → Pizza. Each city has a personality."
>
> "This is the bridge to senior analyst work. Once you have window functions in your toolkit, you can answer 'top N per group', 'compare to previous row', 'running totals' — all the things that tell stories instead of just totals."

### The 9-concept recap

> "Okay. We're at 56 minutes. Let me read you the list of nine SQL concepts you used in the last hour."
>
> [look at the audience, not the screen]
>
> "**One.** SELECT-FROM. **Two.** WHERE. **Three.** COUNT, SUM, AVG. **Four.** GROUP BY. **Five.** ORDER BY and LIMIT. **Six.** INNER JOIN. **Seven.** LEFT JOIN. **Eight.** Common Table Expressions — `WITH`. **Nine.** Window functions — `OVER PARTITION BY`."
>
> "Plus a bonus: `CASE WHEN`. That's the rating-bucket query at the bottom of the notebook — bucketing values into named ranges."
>
> "If two weeks from now you can look at a table and ask any of these nine kinds of questions, you are functioning as a data analyst. Truly."

### Closing

> "Final thing. Repeat after me, in your head, this idea — because it's the thing I want you to walk out with:"
>
> "**SQL isn't a language you memorise. It's a way of asking questions of a table.** Every query you ever write is some combination of: which columns do I want, which table, with what filter, grouped by what, joined to what else. That's the whole shape. The more questions you ask, the more fluent you get."
>
> "The notebook you have in front of you is yours to keep. There's a cheatsheet inside it. There's a folder of 20 practice problems with full solutions. There's a `run_locally.md` if you'd rather do this in DBeaver or Postgres at your desk. Everything is on the GitHub repo I'll drop in chat."
>
> "Last 4 minutes — questions. Anything. Especially the ones you've been holding back because you thought they were stupid. There are no stupid SQL questions today."
>
> [Q&A]

---

# Speaker tips appendix

## If Colab is slow

- Don't wait. Move on. Tell the room: "While the data downloads in the background, let me show you what we're going to build" and project the **already-loaded** notebook on your machine.
- Worst case: have everyone watch your screen for the first 10 minutes while their downloads finish.
- If the projector laptop's Colab is slow too, switch to **Jupyter running locally** with the SQLite DB you pre-built. The queries are identical.

## If a learner derails with an off-topic question

- Acknowledge once, redirect: "That's a great question — different topic, let me grab you in the break." Then look back at the slide.
- Off-topic favorites in this session: indexing, NoSQL, partitioning strategies, ORM vs raw SQL. They're real, they're not for hour 1.

## If you're 5 minutes behind schedule

- Skip the **try-this** mini-exercises in Acts 2 and 3 (everyone gets the notebook anyway).
- Do not skip Q8 (CTEs). That's the whole point of the second half.
- Do not skip the closing recap. People need the 9-concept summary to consolidate.

## If a learner spots a bug in your query

- **Thank them by name.** Out loud. "You're right, my mistake — let me fix that."
- Never bluff your way past it. They'll lose trust and so will the rest of the room.
- Fix it live. Re-run. Move on.

## "What about NoSQL?" — it will come

- Expect it 25-35 minutes in. Have a one-paragraph answer ready:
- "Different shape of database. SQL is for structured tabular data with relationships — what most business analytics looks like. NoSQL is for documents (MongoDB), key-value (Redis), graphs (Neo4j), or massive append-only logs (Cassandra). Most companies use both. The skills overlap less than you'd think — you'd usually pick the database first based on your data shape, then learn its query language. Today is SQL."
- Don't go deeper unless someone presses. The session is about SQL fluency, not database taxonomy.

## "Should we be writing tests for our SQL?"

- "Yes — at the analyst level it's mostly spot-checks (does the row count match what you'd expect?), at the engineer level there are tools like dbt that test queries the way unit tests test code. Worth Googling 'dbt tests' after this session."

## "Is ChatGPT going to replace this skill?"

- It will come. You decide your own honest answer; here's a true one:
- "ChatGPT will write you a `SELECT … GROUP BY` faster than you can. What it can't do is **know whether the answer is right** — for that you need to read the SQL, understand the joins, and sanity-check the numbers. The hour you just spent is exactly that skill. Worth keeping."

## Energy management

- 60 minutes of continuous talking is hard. Drink water at every Act break.
- The 12-minute mark (mid-Act 2) and the 45-minute mark (mid-Act 4) are the two natural energy dips for the room. Make eye contact, ask a check-in question, walk a few steps.
- Don't skip the silly opening "show of hands" — it changes the room from passive watching to active participation, and that pays back ten times over by Act 3.
