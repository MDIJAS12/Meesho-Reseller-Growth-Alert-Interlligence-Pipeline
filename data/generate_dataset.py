import random
import sqlite3
import csv
import os

rng = random.Random(42)
OUTDIR = os.path.dirname(os.path.abspath(__file__))

REGIONS = ["North", "South", "East", "West"]
CITIES = {
    "North": ["Delhi", "Jaipur", "Lucknow"],
    "South": ["Bengaluru", "Chennai", "Hyderabad"],
    "East": ["Kolkata", "Patna", "Bhubaneswar"],
    "West": ["Mumbai", "Pune", "Ahmedabad"],
}
CATEGORIES = ["Ethnic Wear", "Western Wear", "Kids Wear", "Home & Kitchen", "Beauty & Personal Care"]
CAT_PRICE_RANGE = {
    "Ethnic Wear": (399, 1499), "Western Wear": (349, 1299), "Kids Wear": (249, 899),
    "Home & Kitchen": (199, 1999), "Beauty & Personal Care": (149, 799),
}
STATUSES = ["Delivered", "Returned", "Cancelled", "Pending"]
STATUS_WEIGHTS = [0.70, 0.15, 0.10, 0.05]
MONTHS = ["April", "May", "June"]
MONTH_DAYS = {"April": 30, "May": 31, "June": 30}

resellers = []
rid_counter = 1
for region in REGIONS:
    for i in range(6):
        rid = f"RS{rid_counter:03d}"
        city = CITIES[region][i % 3]
        join_month = rng.choice(["2026-01", "2026-02", "2026-03"])
        join_date = f"{join_month}-{rng.randint(1,28):02d}"
        resellers.append({"reseller_id": rid, "reseller_name": f"{city} Reseller {i+1}",
                           "city": city, "region": region, "join_date": join_date})
        rid_counter += 1

ZERO_ORDER_RESELLER = resellers[-1]["reseller_id"]
order_pool_resellers = [r for r in resellers if r["reseller_id"] != ZERO_ORDER_RESELLER]

CAT_WEIGHTS_BY_MONTH = {
    "April": {"Ethnic Wear": 0.20, "Western Wear": 0.24, "Kids Wear": 0.20, "Home & Kitchen": 0.20, "Beauty & Personal Care": 0.16},
    "May":   {"Ethnic Wear": 0.34, "Western Wear": 0.20, "Kids Wear": 0.16, "Home & Kitchen": 0.14, "Beauty & Personal Care": 0.16},
    "June":  {"Ethnic Wear": 0.18, "Western Wear": 0.22, "Kids Wear": 0.20, "Home & Kitchen": 0.22, "Beauty & Personal Care": 0.18},
}
ORDERS_PER_MONTH = 300

orders = []
oid_counter = 1
for month in MONTHS:
    cats = list(CAT_WEIGHTS_BY_MONTH[month].keys())
    weights = list(CAT_WEIGHTS_BY_MONTH[month].values())
    for _ in range(ORDERS_PER_MONTH):
        reseller = rng.choice(order_pool_resellers)
        category = rng.choices(cats, weights=weights, k=1)[0]
        lo, hi = CAT_PRICE_RANGE[category]
        unit_price = round(rng.uniform(lo, hi), 2)
        quantity = rng.choices([1, 2, 3, 4], weights=[0.55, 0.25, 0.13, 0.07], k=1)[0]
        day = rng.randint(1, MONTH_DAYS[month])
        order_date = f"2026-{MONTHS.index(month)+4:02d}-{day:02d}"
        status = rng.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        orders.append({"order_id": f"ORD{oid_counter:05d}", "reseller_id": reseller["reseller_id"],
                        "category": category, "product_name": f"{category} Item {rng.randint(1,999)}",
                        "quantity": quantity, "unit_price": unit_price, "order_date": order_date,
                        "month": month, "status": status})
        oid_counter += 1

with open(os.path.join(OUTDIR, "resellers.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["reseller_id", "reseller_name", "city", "region", "join_date"])
    w.writeheader(); w.writerows(resellers)

with open(os.path.join(OUTDIR, "orders.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["order_id", "reseller_id", "category", "product_name",
                                       "quantity", "unit_price", "order_date", "month", "status"])
    w.writeheader(); w.writerows(orders)

db_path = os.path.join(OUTDIR, "meesho_reseller.db")
if os.path.exists(db_path):
    os.remove(db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("""CREATE TABLE resellers (reseller_id TEXT PRIMARY KEY, reseller_name TEXT,
               city TEXT, region TEXT, join_date TEXT)""")
cur.execute("""CREATE TABLE orders (order_id TEXT PRIMARY KEY, reseller_id TEXT, category TEXT,
               product_name TEXT, quantity INTEGER, unit_price REAL, order_date TEXT,
               month TEXT, status TEXT,
               FOREIGN KEY (reseller_id) REFERENCES resellers(reseller_id))""")
cur.executemany("INSERT INTO resellers VALUES (:reseller_id,:reseller_name,:city,:region,:join_date)", resellers)
cur.executemany("""INSERT INTO orders VALUES (:order_id,:reseller_id,:category,:product_name,
                    :quantity,:unit_price,:order_date,:month,:status)""", orders)
conn.commit()
conn.close()
print(f"Wrote {len(resellers)} resellers and {len(orders)} orders. Zero-order reseller: {ZERO_ORDER_RESELLER}")
