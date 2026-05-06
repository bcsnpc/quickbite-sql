"""
QuickBite SQL Training — Data Generator
Run: python scripts/generate_data.py
Outputs 9 CSVs to data/ folder. Reproducible with seed=42.
"""

import random
import sqlite3
import os
from datetime import date, timedelta, datetime

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ─── helpers ────────────────────────────────────────────────────────────────

def rand_date(start: str, end: str) -> str:
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    return (s + timedelta(days=random.randint(0, (e - s).days))).isoformat()


def rand_dates_array(start: str, end: str, n: int) -> list:
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    span = (e - s).days
    offsets = np.random.randint(0, span + 1, n)
    return [(s + timedelta(days=int(o))).isoformat() for o in offsets]


FIRST_NAMES = [
    "Aarav", "Arjun", "Aditya", "Akash", "Amitabh", "Ananya", "Anjali", "Ankit",
    "Aryan", "Ashwin", "Deepa", "Deepak", "Divya", "Farhan", "Gaurav", "Harini",
    "Ishaan", "Karthik", "Kavya", "Kunal", "Lakshmi", "Manish", "Meera", "Mihir",
    "Mohit", "Nandini", "Neha", "Nikhil", "Nitya", "Pooja", "Prachi", "Priya",
    "Rahul", "Raj", "Rajesh", "Ravi", "Rohit", "Sakshi", "Saloni", "Sanjay",
    "Shreya", "Shweta", "Siddharth", "Sneha", "Suresh", "Swati", "Tanvi", "Uday",
    "Varun", "Vijay", "Vikram", "Vishal", "Vivek", "Yamini", "Zara", "Zoya",
    "Bhavna", "Chetan", "Dhruv", "Esha", "Fatima", "Geeta", "Hemant", "Indira",
    "Jaya", "Kabir", "Lavanya", "Madhuri", "Nalini", "Omkar", "Pankaj", "Radha",
    "Sunita", "Tarun", "Uma", "Venkat", "Waqar", "Xenia", "Yash", "Zubair"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Shah", "Mehta",
    "Joshi", "Rao", "Reddy", "Nair", "Pillai", "Iyer", "Menon", "Krishnan",
    "Agarwal", "Bose", "Chatterjee", "Das", "Dutta", "Ghosh", "Mukherjee",
    "Banerjee", "Chakraborty", "Sen", "Roy", "Mishra", "Tiwari", "Pandey",
    "Dubey", "Chaudhary", "Yadav", "Srivastava", "Tripathi", "Saxena",
    "Khanna", "Malhotra", "Kapoor", "Anand", "Bhat", "Hegde", "Kamath",
    "Shetty", "Naik", "Rajan", "Subramaniam", "Venkatesh", "Ramesh", "Suresh"
]


def random_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def name_to_email(name: str, idx: int) -> str:
    # RFC 2606 reserves example.com / example.org for documentation — safe synthetic data
    parts = name.lower().split()
    domain = random.choice(["example.com", "example.org"])
    base = f"{parts[0]}.{parts[1]}{random.randint(1, 99)}"
    return f"{base}@{domain}"


# ─── PHASE 1: cities ────────────────────────────────────────────────────────

print("Generating cities.csv ...")
cities_data = [
    ("CTY01", "Hyderabad",  "Telangana",    17.385, 78.486, "Tier1", "2022-06-01"),
    ("CTY02", "Bangalore",  "Karnataka",    12.972, 77.594, "Tier1", "2022-06-01"),
    ("CTY03", "Mumbai",     "Maharashtra",  19.076, 72.877, "Tier1", "2022-07-01"),
    ("CTY04", "Delhi",      "Delhi",        28.704, 77.103, "Tier1", "2022-07-15"),
    ("CTY05", "Chennai",    "Tamil Nadu",   13.083, 80.270, "Tier1", "2022-08-01"),
    ("CTY06", "Pune",       "Maharashtra",  18.520, 73.856, "Tier1", "2022-09-01"),
    ("CTY07", "Kolkata",    "West Bengal",  22.573, 88.364, "Tier1", "2022-10-01"),
    ("CTY08", "Ahmedabad",  "Gujarat",      23.026, 72.572, "Tier2", "2023-01-01"),
]
cities_df = pd.DataFrame(cities_data, columns=[
    "city_id", "city_name", "state", "latitude", "longitude", "tier", "launched_date"
])
cities_df.to_csv(os.path.join(DATA_DIR, "cities.csv"), index=False)
print(f"  cities.csv: {len(cities_df)} rows")

CITY_NAMES = [r[1] for r in cities_data]
# Tier1 cities get more weight; Ahmedabad (Tier2) gets less
CITY_WEIGHTS = [0.16, 0.16, 0.15, 0.15, 0.12, 0.11, 0.10, 0.05]


# ─── PHASE 2: customers ─────────────────────────────────────────────────────

print("Generating customers.csv ...")
N_CUSTOMERS = 10000
cust_names = [random_name() for _ in range(N_CUSTOMERS)]
cust_cities = random.choices(CITY_NAMES, weights=CITY_WEIGHTS, k=N_CUSTOMERS)
cust_signup = rand_dates_array("2023-01-01", "2026-04-15", N_CUSTOMERS)

# Age skewed toward 22-40
ages_raw = np.random.normal(30, 8, N_CUSTOMERS)
ages = np.clip(ages_raw, 18, 65).astype(int)

customers_df = pd.DataFrame({
    "customer_id": [f"C{i:05d}" for i in range(1, N_CUSTOMERS + 1)],
    "name": cust_names,
    "email": [name_to_email(n, i) for i, n in enumerate(cust_names)],
    "city": cust_cities,
    "signup_date": cust_signup,
    "age": ages,
})
customers_df.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)
print(f"  customers.csv: {len(customers_df)} rows")

ALL_CUSTOMER_IDS = customers_df["customer_id"].tolist()


# ─── PHASE 3: restaurants ───────────────────────────────────────────────────

print("Generating restaurants.csv ...")

CUISINES = ["Biryani", "South Indian", "North Indian", "Chinese", "Italian",
            "Continental", "Street Food", "Mughlai", "Desserts", "Pizza"]

RESTAURANT_NAMES_BY_CUISINE = {
    "Biryani":      ["Paradise Biryani", "Bawarchi", "Mehfil Biryani", "Hyderabadi House",
                     "Biryani Blues", "Dum Pukht", "Royal Biryani", "Biryani Factory",
                     "Golconda Biryani", "Spice Garden"],
    "South Indian": ["Saravana Bhavan", "Murugan Idli Shop", "Adyar Ananda Bhavan",
                     "Sangeetha", "Annapurna", "Udupi Palace", "MTR", "Vidyarthi Bhavan",
                     "Ram Ashraya", "Cafe Madras"],
    "North Indian": ["Moti Mahal", "Punjabi Dhaba", "Delhi 6", "Haveli Restaurant",
                     "Sarson", "Pind Balluchi", "Frontier", "Dhaba Express",
                     "Masala Chowk", "Punjab Grill"],
    "Chinese":      ["Dragon Palace", "Chung Fa", "Mainland China", "The Orient",
                     "Beijing Bites", "Wok To Walk", "Chopsticks", "Golden Dragon",
                     "Bamboo Garden", "Noodle House"],
    "Italian":      ["Trattoria", "La Bella Italia", "Pizza Roma", "Pasta House",
                     "Il Forno", "Olive Garden", "Bello Cibo", "Tuscany",
                     "Milano Cafe", "Pesto Kitchen"],
    "Continental":  ["Truffles", "The Flying Saucer", "Smoke House Deli", "Hard Rock Cafe",
                     "The Humming Tree", "Corner House", "Biere Club", "Windmills",
                     "Toit Brewpub", "Social"],
    "Street Food":  ["Chaat Corner", "Bombay Pav Bhaji", "Vada Pav Hub", "Mumbai Street",
                     "Bhel Puri House", "Sev Puri Stall", "Elco Pani Puri", "Ram Shyam",
                     "Juhu Chowpati", "Chat Pata"],
    "Mughlai":      ["Karim's", "Al Jawahar", "Aslam Chicken", "Mubarak Mahal",
                     "Mughal Darbar", "Nawabi Kitchen", "Shah Jahani", "Lucknowi Dawat",
                     "Dum Biryani House", "Royal Nawab"],
    "Desserts":     ["Natural Ice Cream", "Havmor", "Cream Stone", "Gelato Italiano",
                     "Baskin Robbins Local", "Mithai Junction", "Sweet Spot",
                     "Choco Fantasy", "The Dessert Lab", "Sugar & Spice"],
    "Pizza":        ["Dominos Express", "Pizza Point", "La Pino'z", "Pizza Corner",
                     "Slice of Heaven", "Pizza Town", "The Pizza Company", "Cheese N More",
                     "Oven Story", "Pizza Studio"],
}

# City-cuisine bias
CITY_CUISINE_BIAS = {
    "Hyderabad":  ["Biryani", "Mughlai", "South Indian"],
    "Bangalore":  ["South Indian", "Continental", "Chinese"],
    "Mumbai":     ["Street Food", "North Indian", "Desserts"],
    "Delhi":      ["Mughlai", "North Indian", "Street Food"],
    "Chennai":    ["South Indian", "Biryani", "Chinese"],
    "Pune":       ["Continental", "North Indian", "Pizza"],
    "Kolkata":    ["Street Food", "North Indian", "Chinese"],
    "Ahmedabad":  ["North Indian", "Desserts", "Street Food"],
}

# Distribute 200 restaurants across cities proportionally
CITY_REST_DIST = {
    "Hyderabad": 32, "Bangalore": 32, "Mumbai": 28, "Delhi": 28,
    "Chennai": 22, "Pune": 22, "Kolkata": 20, "Ahmedabad": 16,
}

rest_rows = []
rest_id = 1
for city, count in CITY_REST_DIST.items():
    dominant = CITY_CUISINE_BIAS[city]
    # 60% from dominant cuisines, 40% from others
    other = [c for c in CUISINES if c not in dominant]
    for _ in range(count):
        if random.random() < 0.60:
            cuisine = random.choice(dominant)
        else:
            cuisine = random.choice(other)
        name_pool = RESTAURANT_NAMES_BY_CUISINE[cuisine]
        name = random.choice(name_pool) + (f" - {city}" if random.random() < 0.5 else "")
        rating = round(float(np.clip(np.random.normal(4.0, 0.4), 3.0, 4.9)), 1)
        price_tier = random.choices(["Budget", "Mid", "Premium"], weights=[0.35, 0.45, 0.20])[0]
        onboarded = rand_date("2022-06-01", "2026-03-01")
        is_active = 1 if random.random() < 0.95 else 0
        rest_rows.append((f"R{rest_id:03d}", name, city, cuisine, rating, price_tier, onboarded, is_active))
        rest_id += 1

restaurants_df = pd.DataFrame(rest_rows, columns=[
    "restaurant_id", "name", "city", "cuisine", "rating_avg", "price_tier", "onboarded_date", "is_active"
])
restaurants_df.to_csv(os.path.join(DATA_DIR, "restaurants.csv"), index=False)
print(f"  restaurants.csv: {len(restaurants_df)} rows")

ACTIVE_RESTAURANTS = restaurants_df[restaurants_df["is_active"] == 1]["restaurant_id"].tolist()
REST_CITY_MAP = dict(zip(restaurants_df["restaurant_id"], restaurants_df["city"]))


# ─── PHASE 4: promotions ────────────────────────────────────────────────────

print("Generating promotions.csv ...")

PROMO_CODES = [
    "WEEKEND20", "FIRSTBITE", "BIRYANI50", "LUNCHSPECIAL", "DINNERDEAL",
    "FLAT100", "FLAT200", "NEWUSER30", "LOYAL15", "MONSOON25",
    "SUMMERFEST", "WINTERSALE", "PIZZATIME", "SWIGGYOFF", "FRESHSTART",
    "HAPPYHOURS", "MIDNIGHT20", "EARLYBIRD", "LATENIGHT", "WEEKDAY10",
    "HYDFOOD", "BLRFOOD", "MUMBAIFEST", "DELHIKHAO", "SOUTHINDIAN25",
    "MUGHLAI30", "STREETFOOD", "DESSERT20", "CHINAFEST", "ITALIANI",
    "PREMIUMONLY", "BUDGETMEAL", "COMBO50", "FAMILY200", "SOLO100",
    "UPIBONUS", "CARDPAY", "WALLET20", "CASHBACK", "REFERRAL50",
    "BIRTHDAY30", "ANNIVERSARY", "CELEBRATE", "FESTIVAL25", "HOLIDAY50",
    "SPRINGFEST", "AUTUMNBITE", "WINTERWARM", "SUMMERCOOL", "MONSOONMAGIC",
    "QUICKBITE10", "SPEEDFOOD", "FASTTRACK", "TURBO15", "LIGHTNING",
    "MEGA100", "SUPER200", "ULTRA300", "PRIME50", "GOLD25",
    "SILVER15", "BRONZE10", "PLATINUM", "DIAMOND100", "CRYSTAL50",
    "NEWCITY", "LAUNCH50", "GRAND100", "OPENING200", "INTRO25",
    "HOTDEAL", "FLASHSALE", "LIMITED", "EXCLUSIVE", "SPECIAL30",
    "HEALTHY20", "VEGSPECIAL", "NONVEG25", "SEAFOOD30", "ORGANIC15",
    "SPICY10", "MILD15", "SWEET20", "TANGY25", "CRISPY30",
]

promo_rows = []
for i in range(1, 81):
    code = PROMO_CODES[i - 1] if i <= len(PROMO_CODES) else f"PROMO{i:03d}"
    dtype = random.choice(["PERCENTAGE", "FLAT"])
    if dtype == "PERCENTAGE":
        val = random.choice([10, 15, 20, 25, 30, 50])
    else:
        val = random.choice([50, 100, 150, 200, 300])
    min_order = random.choice([0, 200, 300, 500])
    valid_from = rand_date("2025-10-01", "2026-03-01")
    valid_until = rand_date("2026-03-01", "2026-06-30")
    cuisine = random.choice(CUISINES + [None, None, None])  # ~25% have cuisine restriction
    max_uses = random.choice([100, 500, 1000, 2000, 5000, 10000])
    promo_rows.append((
        f"PROMO{i:03d}", code, dtype, val, min_order,
        valid_from, valid_until, cuisine, max_uses
    ))

promotions_df = pd.DataFrame(promo_rows, columns=[
    "promo_id", "promo_code", "discount_type", "discount_value",
    "min_order_value", "valid_from", "valid_until", "applicable_cuisine", "max_uses"
])
promotions_df.to_csv(os.path.join(DATA_DIR, "promotions.csv"), index=False)
print(f"  promotions.csv: {len(promotions_df)} rows")

PROMO_IDS = promotions_df["promo_id"].tolist()


# ─── PHASE 5: orders (behavior buckets) ─────────────────────────────────────

print("Generating orders.csv ...")

SESSION_START = date(2026, 1, 1)
SESSION_END   = date(2026, 4, 27)

# Behavior buckets
REGULARS_COUNT  = 1500   # order 2-3x/week Jan-Apr
CHURNERS_COUNT  = 1200   # order weekly Jan-Feb, zero Mar-Apr
CASUAL_COUNT    = 2000   # every 2-3 weeks
NEWCOMERS_COUNT = 1500   # only Mar-Apr
SPORADIC_COUNT  = 3800   # 1-3 orders anywhere

cids = ALL_CUSTOMER_IDS[:]
random.shuffle(cids)

regulars  = cids[:REGULARS_COUNT]
churners  = cids[REGULARS_COUNT:REGULARS_COUNT+CHURNERS_COUNT]
casual    = cids[REGULARS_COUNT+CHURNERS_COUNT:REGULARS_COUNT+CHURNERS_COUNT+CASUAL_COUNT]
newcomers = cids[REGULARS_COUNT+CHURNERS_COUNT+CASUAL_COUNT:REGULARS_COUNT+CHURNERS_COUNT+CASUAL_COUNT+NEWCOMERS_COUNT]
sporadic  = cids[REGULARS_COUNT+CHURNERS_COUNT+CASUAL_COUNT+NEWCOMERS_COUNT:]


def random_order_time() -> str:
    """Return HH:MM:SS biased toward lunch (12-14) and dinner (19-22)."""
    slot = random.random()
    if slot < 0.40:  # dinner
        h = random.randint(19, 22)
    elif slot < 0.70:  # lunch
        h = random.randint(12, 14)
    elif slot < 0.85:  # evening snack
        h = random.randint(16, 18)
    else:  # late night / breakfast
        h = random.randint(7, 11)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return f"{h:02d}:{m:02d}:{s:02d}"


def make_order(order_id: int, customer_id: str, order_date: date) -> dict:
    rest_id = random.choice(ACTIVE_RESTAURANTS)
    status = random.choices(
        ["DELIVERED", "CANCELLED", "REFUNDED"],
        weights=[88, 8, 4]
    )[0]
    promo = random.choices([None, random.choice(PROMO_IDS)], weights=[70, 30])[0]
    amount = round(float(np.random.lognormal(mean=6.5, sigma=0.5)), 2)
    amount = max(100.0, min(3000.0, amount))
    if promo:
        discount = round(amount * random.uniform(0.05, 0.25), 2)
        amount = round(max(100.0, amount - discount), 2)
    payment = random.choices(
        ["UPI", "CARD", "CASH", "WALLET"],
        weights=[60, 25, 10, 5]
    )[0]
    return {
        "order_id": f"O{order_id:07d}",
        "customer_id": customer_id,
        "restaurant_id": rest_id,
        "order_date": order_date.isoformat(),
        "order_time": random_order_time(),
        "total_amount": amount,
        "status": status,
        "promo_id": promo,
        "payment_method": payment,
    }


order_rows = []
order_id = 1

# Regulars: 2-3 orders/week throughout Jan-Apr
print("  Building regular orders ...")
for cid in regulars:
    cur = SESSION_START
    while cur <= SESSION_END:
        n_this_week = random.randint(2, 3)
        for _ in range(n_this_week):
            day_offset = random.randint(0, 6)
            order_date = cur + timedelta(days=day_offset)
            if order_date > SESSION_END:
                break
            order_rows.append(make_order(order_id, cid, order_date))
            order_id += 1
        cur += timedelta(days=7)

# Churners: 1-2 orders/week Jan-Feb, zero Mar-Apr
print("  Building churner orders ...")
CHURN_END = date(2026, 2, 28)
for cid in churners:
    cur = SESSION_START
    while cur <= CHURN_END:
        n_this_week = random.randint(1, 2)
        for _ in range(n_this_week):
            day_offset = random.randint(0, 6)
            order_date = cur + timedelta(days=day_offset)
            if order_date > CHURN_END:
                break
            order_rows.append(make_order(order_id, cid, order_date))
            order_id += 1
        cur += timedelta(days=7)

# Casual: order every 2-3 weeks
print("  Building casual orders ...")
for cid in casual:
    cur = SESSION_START
    while cur <= SESSION_END:
        order_date = cur + timedelta(days=random.randint(0, 6))
        if order_date <= SESSION_END:
            order_rows.append(make_order(order_id, cid, order_date))
            order_id += 1
        cur += timedelta(days=random.randint(14, 21))

# Newcomers: only Mar-Apr
print("  Building newcomer orders ...")
NEWCOMER_START = date(2026, 3, 1)
for cid in newcomers:
    n_orders = random.randint(2, 8)
    for _ in range(n_orders):
        day_offset = random.randint(0, (SESSION_END - NEWCOMER_START).days)
        order_date = NEWCOMER_START + timedelta(days=day_offset)
        order_rows.append(make_order(order_id, cid, order_date))
        order_id += 1

# Sporadic: 1-3 orders anywhere
print("  Building sporadic orders ...")
for cid in sporadic:
    n_orders = random.randint(1, 3)
    for _ in range(n_orders):
        order_date_str = rand_date("2026-01-01", "2026-04-27")
        order_date = date.fromisoformat(order_date_str)
        order_rows.append(make_order(order_id, cid, order_date))
        order_id += 1

# Top-up April 27 to guarantee 800-1200 orders on "yesterday"
TARGET_DATE = "2026-04-27"
count_yesterday = sum(1 for r in order_rows if r["order_date"] == TARGET_DATE)
if count_yesterday < 800:
    needed = 900 - count_yesterday
    print(f"  April 27 top-up: adding {needed} orders (was {count_yesterday})")
    topup_customers = random.choices(ALL_CUSTOMER_IDS, k=needed)
    for cid in topup_customers:
        order_rows.append(make_order(order_id, cid, date(2026, 4, 27)))
        order_id += 1

orders_df = pd.DataFrame(order_rows)
orders_df = orders_df.sample(frac=1, random_state=42).reset_index(drop=True)
# Reassign order IDs in shuffled order so they look random
orders_df["order_id"] = [f"O{i:07d}" for i in range(1, len(orders_df) + 1)]
orders_df.to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)
print(f"  orders.csv: {len(orders_df)} rows")

ORDER_IDS       = orders_df["order_id"].tolist()
ORDER_REST_MAP  = dict(zip(orders_df["order_id"], orders_df["restaurant_id"]))
ORDER_STATUS    = dict(zip(orders_df["order_id"], orders_df["status"]))
ORDER_AMOUNT    = dict(zip(orders_df["order_id"], orders_df["total_amount"]))
REST_CUISINE_MAP = dict(zip(restaurants_df["restaurant_id"], restaurants_df["cuisine"]))


# ─── PHASE 6: order_items ────────────────────────────────────────────────────

print("Generating order_items.csv ...")

MENU_BY_CUISINE = {
    "Biryani":      ["Hyderabadi Dum Biryani", "Chicken Biryani", "Mutton Biryani",
                     "Veg Biryani", "Egg Biryani", "Prawn Biryani", "Raita", "Mirchi Ka Salan"],
    "South Indian": ["Masala Dosa", "Plain Dosa", "Idli Sambar", "Vada", "Uttapam",
                     "Pongal", "Chettinad Chicken", "Filter Coffee", "Rasam Rice"],
    "North Indian": ["Butter Chicken", "Dal Makhani", "Paneer Butter Masala", "Naan",
                     "Tandoori Roti", "Chole Bhature", "Rajma Chawal", "Palak Paneer"],
    "Chinese":      ["Chicken Manchurian", "Veg Fried Rice", "Chicken Fried Rice",
                     "Noodles", "Spring Roll", "Dimsums", "Chilli Paneer", "Momos"],
    "Italian":      ["Margherita Pizza", "Pasta Arrabiata", "Spaghetti Bolognese",
                     "Lasagna", "Garlic Bread", "Risotto", "Bruschetta", "Tiramisu"],
    "Continental":  ["Grilled Chicken", "Fish and Chips", "Caesar Salad", "Burger",
                     "Steak", "Mushroom Soup", "Club Sandwich", "Pasta Alfredo"],
    "Street Food":  ["Pav Bhaji", "Vada Pav", "Pani Puri", "Bhel Puri", "Sev Puri",
                     "Dahi Puri", "Aloo Tikki", "Corn Chaat", "Kulfi"],
    "Mughlai":      ["Chicken Kebab", "Seekh Kebab", "Haleem", "Nihari", "Korma",
                     "Shami Kebab", "Mutton Rogan Josh", "Phirni", "Sheer Khurma"],
    "Desserts":     ["Natural Ice Cream", "Gulab Jamun", "Rasgulla", "Halwa",
                     "Kheer", "Jalebi", "Kulfi", "Brownie Sundae", "Waffle"],
    "Pizza":        ["Pepperoni Pizza", "Cheese Burst", "BBQ Chicken Pizza",
                     "Veggie Supreme", "Garlic Bread", "Pasta", "Cold Drink", "Brownie"],
}

BASE_PRICE_BY_CUISINE = {
    "Biryani": (180, 380), "South Indian": (80, 200), "North Indian": (150, 320),
    "Chinese": (120, 280), "Italian": (200, 450), "Continental": (250, 500),
    "Street Food": (50, 150), "Mughlai": (200, 420), "Desserts": (60, 200),
    "Pizza": (150, 450),
}

item_rows = []
for oid in ORDER_IDS:
    rest_id = ORDER_REST_MAP[oid]
    cuisine = REST_CUISINE_MAP.get(rest_id, "North Indian")
    menu = MENU_BY_CUISINE.get(cuisine, MENU_BY_CUISINE["North Indian"])
    lo, hi = BASE_PRICE_BY_CUISINE.get(cuisine, (100, 300))
    n_items = random.randint(1, 4)
    chosen_items = random.choices(menu, k=n_items)
    for item in chosen_items:
        qty = random.randint(1, 3)
        price = round(float(np.random.uniform(lo, hi)), 2)
        item_rows.append({"order_id": oid, "item_name": item,
                          "quantity": qty, "item_price": price})

order_items_df = pd.DataFrame(item_rows)
order_items_df.to_csv(os.path.join(DATA_DIR, "order_items.csv"), index=False)
print(f"  order_items.csv: {len(order_items_df)} rows")


# ─── PHASE 7: ratings ───────────────────────────────────────────────────────

print("Generating ratings.csv ...")

DELIVERED_ORDERS = orders_df[orders_df["status"] == "DELIVERED"]["order_id"].tolist()
# ~70% of delivered orders get a rating
rated_orders = random.sample(DELIVERED_ORDERS, int(len(DELIVERED_ORDERS) * 0.70))

REVIEWS = [
    "Great food!", "Loved it!", "Will order again.", "Fantastic delivery.",
    "Food was cold.", "Took too long.", "Amazing biryani!", "Average taste.",
    "Value for money.", "Excellent packaging.", "Fresh and hot!",
    "Could be better.", "Nice flavours.", "Highly recommended!",
    "Delivery was quick.", "Not as expected.", "Perfect for family.",
    "Portions are good.", "Too spicy for me.", "Mild and tasty.",
]

REST_RATING_AVG = dict(zip(restaurants_df["restaurant_id"], restaurants_df["rating_avg"]))

rating_rows = []
for i, oid in enumerate(rated_orders):
    rest_id = ORDER_REST_MAP[oid]
    avg = REST_RATING_AVG.get(rest_id, 4.0)
    stars = int(np.clip(np.random.normal(avg, 0.7), 1, 5))
    review = None if random.random() < 0.60 else random.choice(REVIEWS)
    order_date = orders_df.loc[orders_df["order_id"] == oid, "order_date"].values[0]
    rated_at = f"{order_date}T{random_order_time()}"
    rating_rows.append({
        "rating_id": f"RT{i+1:05d}",
        "order_id": oid,
        "stars": stars,
        "review_text": review,
        "rated_at": rated_at,
    })

ratings_df = pd.DataFrame(rating_rows)
ratings_df.to_csv(os.path.join(DATA_DIR, "ratings.csv"), index=False)
print(f"  ratings.csv: {len(ratings_df)} rows")


# ─── PHASE 8: delivery_partners ─────────────────────────────────────────────

print("Generating delivery_partners.csv ...")
N_PARTNERS = 500
partner_rows = []
for i in range(1, N_PARTNERS + 1):
    city = random.choices(CITY_NAMES, weights=CITY_WEIGHTS)[0]
    vehicle = random.choices(["Bike", "Scooter", "Bicycle"], weights=[70, 25, 5])[0]
    joined = rand_date("2022-06-01", "2026-03-01")
    is_active = 1 if random.random() < 0.90 else 0
    partner_rows.append((f"D{i:03d}", random_name(), city, vehicle, joined, is_active))

delivery_partners_df = pd.DataFrame(partner_rows, columns=[
    "partner_id", "name", "city", "vehicle", "joined_date", "is_active"
])
delivery_partners_df.to_csv(os.path.join(DATA_DIR, "delivery_partners.csv"), index=False)
print(f"  delivery_partners.csv: {len(delivery_partners_df)} rows")

ACTIVE_PARTNERS    = delivery_partners_df[delivery_partners_df["is_active"] == 1]["partner_id"].tolist()
PARTNER_CITY_MAP   = dict(zip(delivery_partners_df["partner_id"], delivery_partners_df["city"]))


# ─── PHASE 9: delivery_assignments ──────────────────────────────────────────

print("Generating delivery_assignments.csv ...")

# Only delivered and refunded orders get assignments
ASSIGNABLE = orders_df[orders_df["status"].isin(["DELIVERED", "REFUNDED"])]["order_id"].tolist()

assign_rows = []
ORDER_TIME_MAP = dict(zip(orders_df["order_id"], orders_df["order_time"]))
ORDER_DATE_MAP = dict(zip(orders_df["order_id"], orders_df["order_date"]))

for i, oid in enumerate(ASSIGNABLE):
    partner_id = random.choice(ACTIVE_PARTNERS)
    order_date = ORDER_DATE_MAP[oid]
    order_time = ORDER_TIME_MAP[oid]
    # pickup ~10-20 min after order
    base_dt = datetime.fromisoformat(f"{order_date}T{order_time}")
    pickup_dt = base_dt + timedelta(minutes=random.randint(10, 20))
    delivery_minutes = random.randint(10, 55)
    delivery_dt = pickup_dt + timedelta(minutes=delivery_minutes)
    distance = round(random.uniform(0.5, 12.0), 2)
    d_status = "COMPLETED" if random.random() < 0.97 else "FAILED"
    assign_rows.append({
        "assignment_id": f"A{i+1:07d}",
        "order_id": oid,
        "partner_id": partner_id,
        "pickup_time": pickup_dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "delivery_time": delivery_dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "delivery_status": d_status,
        "distance_km": distance,
    })

delivery_assignments_df = pd.DataFrame(assign_rows)
delivery_assignments_df.to_csv(os.path.join(DATA_DIR, "delivery_assignments.csv"), index=False)
print(f"  delivery_assignments.csv: {len(delivery_assignments_df)} rows")


# ─── Summary ────────────────────────────────────────────────────────────────

print("\n=== Row count summary ===")
for fname, df in [
    ("cities.csv", cities_df),
    ("customers.csv", customers_df),
    ("restaurants.csv", restaurants_df),
    ("promotions.csv", promotions_df),
    ("orders.csv", orders_df),
    ("order_items.csv", order_items_df),
    ("ratings.csv", ratings_df),
    ("delivery_partners.csv", delivery_partners_df),
    ("delivery_assignments.csv", delivery_assignments_df),
]:
    print(f"  {fname:<35} {len(df):>8,} rows")


# ─── Verification queries ────────────────────────────────────────────────────

print("\n=== Verification queries ===")
conn = sqlite3.connect(":memory:")
for tname, df in [
    ("cities", cities_df), ("customers", customers_df),
    ("restaurants", restaurants_df), ("promotions", promotions_df),
    ("orders", orders_df), ("order_items", order_items_df),
    ("ratings", ratings_df), ("delivery_partners", delivery_partners_df),
    ("delivery_assignments", delivery_assignments_df),
]:
    df.to_sql(tname, conn, if_exists="replace", index=False)

def q(sql, label):
    result = pd.read_sql_query(sql, conn)
    print(f"\n{label}")
    print(result.to_string(index=False))

q("SELECT COUNT(*) AS cnt FROM orders WHERE order_date = '2026-04-27'",
  "V1: Orders on 2026-04-27 (expect 800-1200):")

q("SELECT COUNT(*) AS cnt FROM orders WHERE status = 'DELIVERED'",
  "V2: Delivered orders (expect ~88000):")

q("SELECT city, COUNT(*) AS n FROM restaurants GROUP BY city ORDER BY n DESC",
  "V3: Restaurants per city:")

q("""
SELECT COUNT(*) AS silent_churners FROM (
    SELECT customer_id FROM orders
    WHERE order_date BETWEEN '2026-01-01' AND '2026-02-28' AND status = 'DELIVERED'
    GROUP BY customer_id HAVING COUNT(*) >= 8
) AS jf
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id FROM orders
    WHERE order_date BETWEEN '2026-03-01' AND '2026-04-27' AND status = 'DELIVERED'
)""", "V4: Silent churners (expect 1000-1500):")

q("""
WITH cr AS (
    SELECT r.city, r.cuisine, SUM(o.total_amount) AS rev
    FROM orders o JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    WHERE o.order_date >= '2026-04-01' AND o.status = 'DELIVERED'
    GROUP BY r.city, r.cuisine
),
rk AS (
    SELECT city, cuisine, rev,
           ROW_NUMBER() OVER (PARTITION BY city ORDER BY rev DESC) AS n
    FROM cr
)
SELECT city, cuisine, ROUND(rev,0) AS revenue FROM rk WHERE n = 1 ORDER BY revenue DESC
""", "V5: Top cuisine per city this month:")

q("""
SELECT dp.city,
       ROUND(AVG((JULIANDAY(da.delivery_time) - JULIANDAY(da.pickup_time)) * 1440), 1) AS avg_delivery_min
FROM delivery_assignments da
JOIN delivery_partners dp ON da.partner_id = dp.partner_id
WHERE da.delivery_status = 'COMPLETED'
GROUP BY dp.city ORDER BY avg_delivery_min
""", "V6: Avg delivery time per city (expect 25-50 min):")

conn.close()
print("\nData generation complete.")
