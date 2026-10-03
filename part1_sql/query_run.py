import sqlite3
import csv
import os

# Find the project folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "output"
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)


# Query 1: Monthly revenue by category
query1 = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY month, category;
"""

rows1 = conn.execute(query1).fetchall()

output1 = os.path.join(OUTPUT_DIR, "monthly_category_revenue.csv")

with open(output1, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["month", "category", "revenue", "n_orders"])
    writer.writerows(rows1)

print(f"Query 1: Wrote {len(rows1)} rows to {output1}")


# Query 2: Region-wise total revenue and order count
query2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
"""

rows2 = conn.execute(query2).fetchall()

output2 = os.path.join(OUTPUT_DIR, "region_revenue_orders.csv")

with open(output2, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["region", "total_revenue", "n_orders"])
    writer.writerows(rows2)

print(f"Query 2: Wrote {len(rows2)} rows to {output2}")


# Query 3: Top resellers by total spend (total spend > 50,000)
query3 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

rows3 = conn.execute(query3).fetchall()

output3 = os.path.join(OUTPUT_DIR, "top_5_resellers.csv")

with open(output3, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "total_spend"])
    writer.writerows(rows3)

print(f"Query 3: Wrote {len(rows3)} rows to {output3}")


# Query 4: Resellers who have never placed an order
query4 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

rows4 = conn.execute(query4).fetchall()

output4 = os.path.join(OUTPUT_DIR, "zero_order_resellers.csv")

with open(output4, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["reseller_id", "reseller_name", "region"])
    writer.writerows(rows4)

print(f"Query 4: Wrote {len(rows4)} rows to {output4}")


# Query 4.1: COUNT(*) vs COUNT(order_id)
query4b = """
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;
"""

rows4b = conn.execute(query4b).fetchall()

output4b = os.path.join(OUTPUT_DIR, "count_star_vs_count_order_id.csv")

with open(output4b, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "reseller_id",
        "reseller_name",
        "count_star",
        "count_order_id"
    ])
    writer.writerows(rows4b)

print(f"Query 4B: Wrote {len(rows4b)} rows to {output4b}")


# Query 5: Average Order Value(AOV) for June, Delivered orders only
query5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

rows5 = conn.execute(query5).fetchall()

output5 = os.path.join(OUTPUT_DIR, "june_delivered_aov.csv")

with open(output5, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["june_delivered_aov"])
    writer.writerows(rows5)

print(f"Query 5: Wrote {len(rows5)} rows to {output5}")


# Close the database connection
conn.close()