# Part 1 SQL Output & Business Query Analysis

## Standing Business Queries & Acceptance Verification

### 1. Monthly Category Revenue (`monthly_category_revenue.csv`)
Aggregates revenue and order count grouped by `month` and `category`. Across April, May, and June 2026, it produces exactly 15 rows with total revenue matching ₹1,262,066.92.

### 2. Region-Wise Revenue & Orders (`region_revenue_orders.csv`)
- **North**: ₹337,125.46 (231 orders)
- **West**: ₹333,106.33 (232 orders)
- **South**: ₹316,736.68 (216 orders)
- **East**: ₹275,098.45 (221 orders)
- **Grand Total**: ₹1,262,066.92 across 900 orders.

### 3. Top Resellers with Spend > ₹50,000 (`top_5_resellers.csv`)
1. **RS019** ("Mumbai Reseller 1"): ₹75,295.09
2. **RS022** ("Mumbai Reseller 4"): ₹73,882.33
3. **RS012** ("Hyderabad Reseller 6"): ₹69,936.46
4. **RS006** ("Lucknow Reseller 6"): ₹64,238.97
5. **RS005** ("Jaipur Reseller 5"): ₹61,825.02

### 4. Zero-Order Reseller & LEFT JOIN Diagnostic (`zero_order_resellers.csv` and `count_star_vs_count_order_id.csv`)
- **Zero-Order Reseller**: `RS024` ("Ahmedabad Reseller 6", Region West).
- **Diagnostic Result**: `COUNT(*) = 1`, `COUNT(order_id) = 0`.

#### Why `COUNT(*)` cannot be used to detect zero-match rows:
In SQL, a `LEFT JOIN` preserves all rows from the left table (`resellers`). When a reseller has placed no orders, SQLite constructs a synthetic result row pairing the reseller attributes with `NULL` for all columns of the right table (`orders`).
- `COUNT(*)` counts the total number of rows returned by the query, including rows consisting entirely of `NULL` values on the right-hand side. Because the unmatched reseller still generates one joined row, `COUNT(*)` evaluates to **1**.
- `COUNT(column_name)` counts only non-NULL entries in the specified column. Because `o.order_id` is `NULL` for unmatched resellers, `COUNT(o.order_id)` evaluates to **0**.
Therefore, testing for zero matches using `COUNT(*) = 0` will always fail, while `COUNT(order_id) = 0` or `WHERE o.order_id IS NULL` accurately identifies resellers who have never placed an order.

### 5. June Delivered AOV (`june_delivered_aov.csv`)
- Filter: `month = "June" AND status = "Delivered"`
- Metric: `SUM(quantity * unit_price) / COUNT(*)`
- Result: **₹1,267.69**
