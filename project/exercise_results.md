# Exercise Results

## Exercise 1: "How many customers do we have?"

### Using DISTINCT

```sql
SELECT 
    COUNT(DISTINCT id) AS customer_count
FROM retaildb.main.dim_customer;
```

| customer_count |
|----------------|
| 9074           |


### Only current customers

```sql
SELECT COUNT(*) AS current_customers
FROM retaildb.main.dim_customer
WHERE valid_to IS NULL;
```

| current_customers |
|-------------------|
| 9074              |


```sql
SELECT 
    COUNT(DISTINCT id) AS customer_count
FROM retaildb.main.dim_customer
WHERE total_purchases > 0;
```

| customer_count |
|----------------|
| 663            |


```sql
SELECT
    count(distinct customer_id) as num_customers
FROM retaildb.main.fact_customer_action
WHERE action_type = 'purchase'
```

| num_customers |
|---------------|
| 663           |


---

## Exercise 2: "What do we sell?"

### Category summary

```sql
SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    MIN(price) AS cheapest,
    MAX(price) AS most_expensive
FROM retaildb.main.dim_product
GROUP BY category
ORDER BY product_count DESC;
```

| category    | product_count | avg_price | cheapest | most_expensive |
|-------------|---------------|-----------|----------|----------------|
| accessories | 52            | 98.88     | 9        | 462            |
| smartphones | 47            | 181.7     | 6        | 1642           |
| laptops     | 32            | 189.34    | 11       | 1300           |
| gaming      | 31            | 170.23    | 27       | 534            |
| audio       | 28            | 219.96    | 16       | 2568           |
| tablets     | 13            | 180.54    | 16       | 746            |


### Full catalog scan

```sql
SELECT
    id,
    name,
    category,
    price
FROM retaildb.main.dim_product
ORDER BY category, price DESC;
```

| id        | name                       | category    | price |
|-----------|----------------------------|-------------|-------|
| SKU_00058 | Elite Holder               | accessories | 462   |
| SKU_00126 | Classic Cable              | accessories | 404   |
| SKU_00181 | Elite Strap                | accessories | 344   |
| SKU_00107 | Elite Cable                | accessories | 324   |
| SKU_00151 | Elite Ring                 | accessories | 244   |
| SKU_00140 | Elite Adapter              | accessories | 204   |
| SKU_00176 | Premium Holder             | accessories | 191   |
| SKU_00132 | Pro Ring                   | accessories | 188   |
| SKU_00122 | Pro Hook                   | accessories | 163   |
| SKU_00053 | Basic Ring                 | accessories | 152   |
| SKU_00049 | Classic Adapter            | accessories | 144   |
| SKU_00086 | Premium Adapter            | accessories | 139   |
| SKU_00032 | Classic Clip               | accessories | 131   |
| SKU_00020 | Elite Cable                | accessories | 130   |
| SKU_00193 | Essential Dongle           | accessories | 130   |
| SKU_00035 | Classic Ring               | accessories | 117   |
| SKU_00195 | Pro Cable                  | accessories | 115   |
| SKU_00157 | Essential Adapter          | accessories | 113   |
| SKU_00172 | Elite Strap                | accessories | 107   |
| SKU_00079 | Pro Hook                   | accessories | 100   |
| SKU_00031 | Classic Cable              | accessories | 92    |
| SKU_00147 | Pro Adapter                | accessories | 92    |
| SKU_00027 | Essential Dongle           | accessories | 88    |
| SKU_00059 | Basic Holder               | accessories | 88    |
| SKU_00076 | Elite Holder               | accessories | 65    |
| SKU_00184 | Essential Clip             | accessories | 62    |
| SKU_00116 | Pro Strap                  | accessories | 56    |
| SKU_00005 | Basic Ring                 | accessories | 53    |
| SKU_00028 | Essential Dongle           | accessories | 47    |
| SKU_00167 | Pro Ring                   | accessories | 46    |
| SKU_00081 | Elite Holder               | accessories | 45    |
| SKU_00094 | Classic Cable              | accessories | 44    |
| SKU_00194 | Essential Holder           | accessories | 40    |
| SKU_00166 | Elite Hook                 | accessories | 39    |
| SKU_00095 | Premium Clip               | accessories | 35    |
| SKU_00012 | Basic Dongle               | accessories | 30    |
| SKU_00120 | Basic Clip                 | accessories | 30    |
| SKU_00046 | Classic Strap              | accessories | 28    |
| SKU_00105 | Pro Adapter                | accessories | 28    |
| SKU_00128 | Premium Holder             | accessories | 28    |
| SKU_00161 | Essential Ring             | accessories | 28    |
| SKU_00186 | Classic Ring               | accessories | 24    |
| SKU_00196 | Basic Holder               | accessories | 21    |
| SKU_00048 | Premium Strap              | accessories | 19    |
| SKU_00108 | Classic Holder             | accessories | 19    |
| SKU_00135 | Pro Cable                  | accessories | 19    |
| SKU_00202 | Pro Hook                   | accessories | 17    |
| SKU_00004 | Basic Strap                | accessories | 14    |
| SKU_00200 | Essential Holder           | accessories | 12    |
| SKU_00006 | Essential Adapter          | accessories | 11    |
| SKU_00009 | Pro Clip                   | accessories | 11    |
| SKU_00100 | Basic Strap                | accessories | 9     |
| SKU_00055 | Classic Microphone         | audio       | 2568  |
| SKU_00153 | Premium Earbuds            | audio       | 748   |
| SKU_00093 | Essential Soundbar         | audio       | 262   |
| SKU_00198 | Premium Receiver           | audio       | 240   |
| SKU_00104 | Elite Earbuds              | audio       | 224   |
| SKU_00062 | Elite Turntable            | audio       | 219   |
| SKU_00052 | Classic DAC                | audio       | 186   |
| SKU_00051 | Basic Soundbar             | audio       | 155   |
| SKU_00003 | TechMart Wireless Earbuds  | audio       | 150   |
| SKU_00192 | Premium DAC                | audio       | 124   |
| SKU_00023 | Classic Subwoofer          | audio       | 117   |
| SKU_00038 | Classic Turntable          | audio       | 117   |
| SKU_00018 | Premium Subwoofer          | audio       | 116   |
| SKU_00143 | Basic Soundbar             | audio       | 115   |
| SKU_00178 | Essential Soundbar         | audio       | 107   |
| SKU_00085 | Pro Soundbar               | audio       | 99    |
| SKU_00037 | Elite Amplifier            | audio       | 82    |
| SKU_00019 | Basic Soundbar             | audio       | 81    |
| SKU_00014 | Premium Microphone         | audio       | 78    |
| SKU_00013 | Classic Microphone         | audio       | 62    |
| SKU_00044 | Premium Receiver           | audio       | 56    |
| SKU_00083 | Classic Soundbar           | audio       | 55    |
| SKU_00131 | Essential Turntable        | audio       | 50    |
| SKU_00057 | Classic Soundbar           | audio       | 44    |
| SKU_00188 | Premium Subwoofer          | audio       | 41    |
| SKU_00142 | Basic Earbuds              | audio       | 25    |
| SKU_00171 | Elite Turntable            | audio       | 22    |
| SKU_00158 | Essential Earbuds          | audio       | 16    |
| SKU_00103 | Basic Headset              | gaming      | 534   |
| SKU_00148 | Basic Controller           | gaming      | 444   |
| SKU_00007 | Classic Joystick           | gaming      | 314   |
| SKU_00099 | Basic Capture Card         | gaming      | 307   |
| SKU_00145 | Premium Joystick           | gaming      | 291   |
| SKU_00115 | Classic Mousepad           | gaming      | 289   |
| SKU_00150 | Basic Stream Deck          | gaming      | 276   |
| SKU_00164 | Essential Capture Card     | gaming      | 242   |
| SKU_00180 | Essential Headset          | gaming      | 238   |
| SKU_00123 | Pro Headset                | gaming      | 217   |
| SKU_00070 | Elite Headset              | gaming      | 199   |
| SKU_00146 | Pro Racing Wheel           | gaming      | 199   |
| SKU_00098 | Essential Stream Deck      | gaming      | 186   |
| SKU_00112 | Classic Stream Deck        | gaming      | 174   |
| SKU_00127 | Elite Racing Wheel         | gaming      | 172   |
| SKU_00061 | Premium Capture Card       | gaming      | 144   |
| SKU_00159 | Elite Racing Wheel         | gaming      | 144   |
| SKU_00102 | Elite Joystick             | gaming      | 133   |
| SKU_00154 | Classic Joystick           | gaming      | 104   |
| SKU_00189 | Pro Racing Wheel           | gaming      | 97    |
| SKU_00109 | Premium Racing Wheel       | gaming      | 90    |
| SKU_00096 | Classic Capture Card       | gaming      | 78    |
| SKU_00139 | Essential Mousepad         | gaming      | 74    |
| SKU_00160 | Premium Mousepad           | gaming      | 52    |
| SKU_00156 | Premium Mousepad           | gaming      | 51    |
| SKU_00088 | Elite Stream Deck          | gaming      | 46    |
| SKU_00063 | Premium Joystick           | gaming      | 45    |
| SKU_00024 | Classic Racing Wheel       | gaming      | 44    |
| SKU_00090 | Classic Stream Deck        | gaming      | 38    |
| SKU_00042 | Basic Headset              | gaming      | 28    |
| SKU_00072 | Basic Mousepad             | gaming      | 27    |
| SKU_00001 | TechMart Pro Laptop        | laptops     | 1300  |
| SKU_00175 | Elite Laptop Stand         | laptops     | 904   |
| SKU_00149 | Elite Laptop Stand         | laptops     | 418   |
| SKU_00106 | Basic Laptop Sleeve        | laptops     | 365   |
| SKU_00045 | Elite Docking Station      | laptops     | 344   |
| SKU_00191 | Pro Privacy Screen         | laptops     | 303   |
| SKU_00201 | Basic USB Hub              | laptops     | 294   |
| SKU_00010 | Elite Cooling Pad          | laptops     | 266   |
| SKU_00136 | Elite Cooling Pad          | laptops     | 219   |
| SKU_00121 | Essential Laptop Stand     | laptops     | 197   |
| SKU_00040 | Basic USB Hub              | laptops     | 165   |
| SKU_00080 | Premium Webcam             | laptops     | 139   |
| SKU_00084 | Basic Cooling Pad          | laptops     | 136   |
| SKU_00036 | Elite Docking Station      | laptops     | 129   |
| SKU_00015 | Basic Carry Case           | laptops     | 126   |
| SKU_00199 | Elite Docking Station      | laptops     | 100   |
| SKU_00026 | Pro Carry Case             | laptops     | 98    |
| SKU_00034 | Essential Webcam           | laptops     | 69    |
| SKU_00077 | Classic Webcam             | laptops     | 66    |
| SKU_00047 | Essential Carry Case       | laptops     | 54    |
| SKU_00056 | Premium Privacy Screen     | laptops     | 49    |
| SKU_00162 | Premium Carry Case         | laptops     | 45    |
| SKU_00074 | Essential Docking Station  | laptops     | 40    |
| SKU_00179 | Basic Privacy Screen       | laptops     | 40    |
| SKU_00011 | Basic Webcam               | laptops     | 38    |
| SKU_00078 | Classic USB Hub            | laptops     | 30    |
| SKU_00119 | Premium Laptop Sleeve      | laptops     | 30    |
| SKU_00203 | Basic Cooling Pad          | laptops     | 28    |
| SKU_00118 | Premium Laptop Sleeve      | laptops     | 21    |
| SKU_00144 | Premium Docking Station    | laptops     | 19    |
| SKU_00071 | Basic Docking Station      | laptops     | 16    |
| SKU_00030 | Elite Laptop Sleeve        | laptops     | 11    |
| SKU_00091 | Basic Phone Stand          | smartphones | 1642  |
| SKU_00002 | TechMart Phone X           | smartphones | 1000  |
| SKU_00097 | Basic Stylus               | smartphones | 846   |
| SKU_00025 | Basic Smartwatch           | smartphones | 594   |
| SKU_00060 | Basic Power Bank           | smartphones | 455   |
| SKU_00190 | Basic Screen Protector     | smartphones | 359   |
| SKU_00183 | Essential Phone Mount      | smartphones | 282   |
| SKU_00182 | Classic Phone Mount        | smartphones | 277   |
| SKU_00173 | Pro Phone Case             | smartphones | 239   |
| SKU_00174 | Classic Screen Protector   | smartphones | 201   |
| SKU_00117 | Essential Power Bank       | smartphones | 200   |
| SKU_00017 | Classic Phone Stand        | smartphones | 162   |
| SKU_00021 | Premium Screen Protector   | smartphones | 158   |
| SKU_00138 | Premium Charging Dock      | smartphones | 139   |
| SKU_00129 | Essential Power Bank       | smartphones | 126   |
| SKU_00082 | Elite Smartwatch           | smartphones | 123   |
| SKU_00111 | Essential Phone Stand      | smartphones | 117   |
| SKU_00114 | Basic Power Bank           | smartphones | 111   |
| SKU_00185 | Essential Phone Stand      | smartphones | 110   |
| SKU_00075 | Classic Screen Protector   | smartphones | 109   |
| SKU_00067 | Essential Stylus           | smartphones | 104   |
| SKU_00064 | Essential Screen Protector | smartphones | 101   |
| SKU_00187 | Pro Charging Dock          | smartphones | 100   |
| SKU_00065 | Essential Phone Case       | smartphones | 98    |
| SKU_00130 | Premium Phone Stand        | smartphones | 82    |
| SKU_00170 | Premium Smartwatch         | smartphones | 80    |
| SKU_00134 | Elite Screen Protector     | smartphones | 74    |
| SKU_00054 | Elite Stylus               | smartphones | 65    |
| SKU_00068 | Classic Charging Dock      | smartphones | 65    |
| SKU_00066 | Elite Phone Mount          | smartphones | 61    |
| SKU_00043 | Basic Phone Mount          | smartphones | 59    |
| SKU_00029 | Pro Smartwatch             | smartphones | 57    |
| SKU_00197 | Premium Screen Protector   | smartphones | 53    |
| SKU_00113 | Pro Phone Stand            | smartphones | 34    |
| SKU_00087 | Premium Phone Case         | smartphones | 32    |
| SKU_00165 | Essential Phone Case       | smartphones | 30    |
| SKU_00022 | Classic Power Bank         | smartphones | 27    |
| SKU_00141 | Classic Phone Case         | smartphones | 26    |
| SKU_00124 | Classic Phone Stand        | smartphones | 23    |
| SKU_00169 | Elite Power Bank           | smartphones | 23    |
| SKU_00008 | Essential Phone Mount      | smartphones | 22    |
| SKU_00041 | Basic Power Bank           | smartphones | 18    |
| SKU_00069 | Classic Power Bank         | smartphones | 17    |
| SKU_00092 | Essential Phone Stand      | smartphones | 13    |
| SKU_00152 | Elite Phone Case           | smartphones | 11    |
| SKU_00039 | Pro Charging Dock          | smartphones | 9     |
| SKU_00168 | Premium Screen Protector   | smartphones | 6     |
| SKU_00155 | Premium Folio              | tablets     | 746   |
| SKU_00137 | Classic Drawing Pen        | tablets     | 630   |
| SKU_00163 | Premium Drawing Pen        | tablets     | 245   |
| SKU_00110 | Premium Grip               | tablets     | 241   |
| SKU_00089 | Essential Tablet Case      | tablets     | 98    |
| SKU_00125 | Essential Tablet Mount     | tablets     | 72    |
| SKU_00073 | Basic Drawing Pen          | tablets     | 63    |
| SKU_00016 | Premium Screen Film        | tablets     | 60    |
| SKU_00033 | Basic Tablet Stand         | tablets     | 45    |
| SKU_00133 | Basic Tablet Mount         | tablets     | 45    |
| SKU_00050 | Essential Tablet Case      | tablets     | 44    |
| SKU_00101 | Premium Tablet Case        | tablets     | 42    |
| SKU_00177 | Basic Tablet Stand         | tablets     | 16    |


---

## Exercise 3: "What did customers do on our busiest day?"

### Single-query approach

```sql
WITH daily_totals AS (
    SELECT
        timestamp::DATE AS day,
        COUNT(*) AS total_actions
    FROM retaildb.main.fact_customer_action
    GROUP BY day
    ORDER BY total_actions DESC
    LIMIT 1
)
SELECT
    actions.action_type,
    COUNT(*) AS action_count
FROM retaildb.main.fact_customer_action actions
WHERE actions.timestamp::DATE = (SELECT day FROM daily_totals)
GROUP BY actions.action_type
ORDER BY action_count DESC;
```

| action_type        | action_count |
|--------------------|--------------|
| product_view       | 245          |
| add_to_cart        | 222          |
| visit              | 156          |
| product_comparison | 46           |
| purchase           | 26           |


### Two-step approach

```sql
-- Step 1: Find the busiest day
SELECT timestamp::DATE AS day, COUNT(*) AS cnt
FROM retaildb.main.fact_customer_action
GROUP BY day
ORDER BY cnt DESC
LIMIT 5;

-- Step 2: Use that date (once you know it)
SELECT action_type, COUNT(*) AS cnt
FROM retaildb.main.fact_customer_action
WHERE timestamp::DATE = '2024-12-22'  -- replace with whatever you found
GROUP BY action_type
ORDER BY cnt DESC;
```

| day        | cnt |
|------------|-----|
| 2024-12-22 | 695 |
| 2024-09-22 | 675 |
| 2024-11-23 | 669 |
| 2024-12-21 | 650 |
| 2024-12-02 | 649 |

| action_type        | cnt |
|--------------------|-----|
| product_view       | 245 |
| add_to_cart        | 222 |
| visit              | 156 |
| product_comparison | 46  |
| purchase           | 26  |


---

## Exercise 4: "Are weekends busier than weekdays?"

```sql
SELECT
    CASE
        WHEN EXTRACT(DOW FROM timestamp) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_actions,
    COUNT(*) * 1.0 / COUNT(DISTINCT timestamp::DATE) AS avg_daily_actions
FROM retaildb.main.fact_customer_action
GROUP BY day_type;
```

| day_type | total_actions | avg_daily_actions |
|----------|---------------|-------------------|
| Weekday  | 152675        | 206.0391          |
| Weekend  | 89943         | 303.8615          |


---

## Exercise 5: "Which product category makes us the most money?"

```sql
SELECT
    product.category,
    COUNT(*) AS purchases,
    SUM(product.price * actions.quantity) AS total_revenue,  -- gross (list-price) revenue; for net revenue use: SUM(product.price * actions.quantity * (1 - actions.discount_pct))
    ROUND(AVG(product.price), 2) AS avg_price
FROM retaildb.main.fact_customer_action actions
INNER JOIN retaildb.main.dim_product product ON actions.product_id = product.id
WHERE actions.action_type = 'purchase'
GROUP BY product.category
ORDER BY total_revenue DESC
```

| Error                                                                                            |
|--------------------------------------------------------------------------------------------------|
| Binder Error: Referenced table "product" not found!

LINE 2:     product.category,
            ^ |

| Error                                       |
|---------------------------------------------|
| Parser Error: syntax error at or near "for" |


---

## Exercise 6: "Something weird happened around Black Friday. What do you see?"

### Daily activity around the holiday

```sql
SELECT
    timestamp::DATE AS day,
    COUNT(*) AS total_activity
FROM retaildb.main.fact_customer_action
WHERE timestamp >= '2024-11-15' AND timestamp < '2024-12-15'
GROUP BY day
ORDER BY day;
```

| day        | total_activity |
|------------|----------------|
| 2024-11-15 | 318            |
| 2024-11-16 | 613            |
| 2024-11-17 | 484            |
| 2024-11-18 | 372            |
| 2024-11-19 | 296            |
| 2024-11-20 | 336            |
| 2024-11-21 | 446            |
| 2024-11-22 | 402            |
| 2024-11-23 | 669            |
| 2024-11-24 | 496            |
| 2024-11-25 | 362            |
| 2024-11-26 | 305            |
| 2024-11-27 | 324            |
| 2024-11-28 | 377            |
| 2024-11-29 | 222            |
| 2024-11-30 | 565            |
| 2024-12-01 | 622            |
| 2024-12-02 | 649            |
| 2024-12-03 | 637            |
| 2024-12-04 | 638            |
| 2024-12-05 | 458            |
| 2024-12-06 | 577            |
| 2024-12-07 | 512            |
| 2024-12-08 | 601            |
| 2024-12-09 | 488            |
| 2024-12-10 | 531            |
| 2024-12-11 | 591            |
| 2024-12-12 | 640            |
| 2024-12-13 | 626            |
| 2024-12-14 | 617            |


### Quantify the pattern

```sql
WITH daily AS (
    SELECT timestamp::DATE AS day, COUNT(*) AS cnt
    FROM retaildb.main.fact_customer_action
    GROUP BY day
),
baseline AS (
    SELECT AVG(cnt) AS avg_daily FROM daily
    WHERE day BETWEEN '2024-11-15' AND '2024-11-28'
)
SELECT
    daily.day,
    daily.cnt AS activity,
    ROUND(daily.cnt / baseline.avg_daily, 1) AS multiple_of_average
FROM daily CROSS JOIN baseline
WHERE daily.day BETWEEN '2024-11-25' AND '2024-12-10'
ORDER BY daily.day;
```

| day        | activity | multiple_of_average |
|------------|----------|---------------------|
| 2024-11-25 | 362      | 0.9                 |
| 2024-11-26 | 305      | 0.7                 |
| 2024-11-27 | 324      | 0.8                 |
| 2024-11-28 | 377      | 0.9                 |
| 2024-11-29 | 222      | 0.5                 |
| 2024-11-30 | 565      | 1.4                 |
| 2024-12-01 | 622      | 1.5                 |
| 2024-12-02 | 649      | 1.6                 |
| 2024-12-03 | 637      | 1.5                 |
| 2024-12-04 | 638      | 1.5                 |
| 2024-12-05 | 458      | 1.1                 |
| 2024-12-06 | 577      | 1.4                 |
| 2024-12-07 | 512      | 1.2                 |
| 2024-12-08 | 601      | 1.5                 |
| 2024-12-09 | 488      | 1.2                 |
| 2024-12-10 | 531      | 1.3                 |


---

## Exercise 7: "Are we losing customers at checkout?"

### Customer-level abandonment

```sql
WITH cart_customers AS (
    SELECT DISTINCT customer_id
    FROM retaildb.main.fact_customer_action
    WHERE action_type = 'add_to_cart'
),
purchase_customers AS (
    SELECT DISTINCT customer_id
    FROM retaildb.main.fact_customer_action
    WHERE action_type = 'purchase'
)
SELECT
    (SELECT COUNT(*) FROM cart_customers) AS added_to_cart,
    (SELECT COUNT(*) FROM purchase_customers) AS purchased,
    (SELECT COUNT(*) FROM cart_customers
     WHERE customer_id NOT IN (SELECT customer_id FROM purchase_customers)) AS abandoned,
    ROUND(
        100.0 * (SELECT COUNT(*) FROM purchase_customers)
        / NULLIF((SELECT COUNT(*) FROM cart_customers), 0),
        1
    ) AS cart_to_purchase_pct;
```

| added_to_cart | purchased | abandoned | cart_to_purchase_pct |
|---------------|-----------|-----------|----------------------|
| 7442          | 663       | 6779      | 8.9                  |


### Per-session abandonment (more precise)

```sql
WITH session_actions AS (
    SELECT
        session_id,
        customer_id,
        MAX(CASE WHEN action_type = 'add_to_cart' THEN 1 ELSE 0 END) AS had_cart_add,
        MAX(CASE WHEN action_type = 'purchase' THEN 1 ELSE 0 END) AS had_purchase
    FROM retaildb.main.fact_customer_action
    GROUP BY session_id, customer_id
)
SELECT
    COUNT(*) AS total_sessions,
    SUM(had_cart_add) AS sessions_with_cart,
    SUM(CASE WHEN had_cart_add = 1 AND had_purchase = 1 THEN 1 ELSE 0 END) AS cart_and_purchase,
    SUM(CASE WHEN had_cart_add = 1 AND had_purchase = 0 THEN 1 ELSE 0 END) AS cart_abandoned,
    ROUND(
        100.0 * SUM(CASE WHEN had_cart_add = 1 AND had_purchase = 1 THEN 1 ELSE 0 END)
        / NULLIF(SUM(had_cart_add), 0),
        1
    ) AS cart_conversion_pct
FROM session_actions;
```

| total_sessions | sessions_with_cart | cart_and_purchase | cart_abandoned | cart_conversion_pct |
|----------------|--------------------|-------------------|----------------|---------------------|
| 56998          | 46959              | 4220              | 42739          | 9                   |


---

## Exercise 8: "I keep hearing we had a rough summer. Is that true?"

```sql
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', timestamp)::DATE AS month,
        COUNT(*) AS total_activity,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM retaildb.main.fact_customer_action
    WHERE timestamp < '2025-01-01'
    GROUP BY month
)
SELECT
    month,
    total_activity,
    unique_customers,
    ROUND(100.0 * total_activity /
        AVG(total_activity) OVER () - 100, 1) AS pct_vs_average
FROM monthly
ORDER BY month;
```

| month      | total_activity | unique_customers | pct_vs_average |
|------------|----------------|------------------|----------------|
| 2022-03-01 | 919            | 187              | -87.1          |
| 2022-04-01 | 1128           | 171              | -84.2          |
| 2022-05-01 | 1504           | 194              | -78.9          |
| 2022-06-01 | 1803           | 182              | -74.7          |
| 2022-07-01 | 2267           | 198              | -68.2          |
| 2022-08-01 | 2812           | 278              | -60.6          |
| 2022-09-01 | 3131           | 297              | -56.1          |
| 2022-10-01 | 3440           | 262              | -51.8          |
| 2022-11-01 | 4002           | 377              | -43.9          |
| 2022-12-01 | 5161           | 422              | -27.7          |
| 2023-01-01 | 4859           | 277              | -31.9          |
| 2023-02-01 | 4562           | 298              | -36.1          |
| 2023-03-01 | 5618           | 390              | -21.3          |
| 2023-04-01 | 5776           | 346              | -19.1          |
| 2023-05-01 | 6542           | 365              | -8.3           |
| 2023-06-01 | 6744           | 377              | -5.5           |
| 2023-07-01 | 7001           | 357              | -1.9           |
| 2023-08-01 | 7298           | 431              | 2.3            |
| 2023-09-01 | 8221           | 482              | 15.2           |
| 2023-10-01 | 8206           | 456              | 15             |
| 2023-11-01 | 8759           | 533              | 22.7           |
| 2023-12-01 | 10041          | 671              | 40.7           |
| 2024-01-01 | 8920           | 417              | 25             |
| 2024-02-01 | 8817           | 464              | 23.6           |
| 2024-03-01 | 9812           | 524              | 37.5           |
| 2024-04-01 | 9434           | 517              | 32.2           |
| 2024-05-01 | 10358          | 561              | 45.2           |
| 2024-06-01 | 10708          | 531              | 50.1           |
| 2024-07-01 | 10676          | 512              | 49.6           |
| 2024-08-01 | 11052          | 596              | 54.9           |
| 2024-09-01 | 11985          | 646              | 68             |
| 2024-10-01 | 11656          | 595              | 63.3           |
| 2024-11-01 | 11790          | 692              | 65.2           |
| 2024-12-01 | 17616          | 934              | 146.9          |


### Month-over-month growth rates

```sql
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', timestamp)::DATE AS month,
        COUNT(*) AS total_activity
    FROM retaildb.main.fact_customer_action
    WHERE timestamp < '2025-01-01'
    GROUP BY month
)
SELECT
    month,
    total_activity,
    LAG(total_activity) OVER (ORDER BY month) AS prev_month,
    ROUND(100.0 * (total_activity - LAG(total_activity) OVER (ORDER BY month))
        / NULLIF(LAG(total_activity) OVER (ORDER BY month), 0), 1) AS mom_growth_pct
FROM monthly
ORDER BY month;
```

| month      | total_activity | prev_month | mom_growth_pct |
|------------|----------------|------------|----------------|
| 2022-03-01 | 919            | NULL       | NULL           |
| 2022-04-01 | 1128           | 919        | 22.7           |
| 2022-05-01 | 1504           | 1128       | 33.3           |
| 2022-06-01 | 1803           | 1504       | 19.9           |
| 2022-07-01 | 2267           | 1803       | 25.7           |
| 2022-08-01 | 2812           | 2267       | 24             |
| 2022-09-01 | 3131           | 2812       | 11.3           |
| 2022-10-01 | 3440           | 3131       | 9.9            |
| 2022-11-01 | 4002           | 3440       | 16.3           |
| 2022-12-01 | 5161           | 4002       | 29             |
| 2023-01-01 | 4859           | 5161       | -5.9           |
| 2023-02-01 | 4562           | 4859       | -6.1           |
| 2023-03-01 | 5618           | 4562       | 23.1           |
| 2023-04-01 | 5776           | 5618       | 2.8            |
| 2023-05-01 | 6542           | 5776       | 13.3           |
| 2023-06-01 | 6744           | 6542       | 3.1            |
| 2023-07-01 | 7001           | 6744       | 3.8            |
| 2023-08-01 | 7298           | 7001       | 4.2            |
| 2023-09-01 | 8221           | 7298       | 12.6           |
| 2023-10-01 | 8206           | 8221       | -0.2           |
| 2023-11-01 | 8759           | 8206       | 6.7            |
| 2023-12-01 | 10041          | 8759       | 14.6           |
| 2024-01-01 | 8920           | 10041      | -11.2          |
| 2024-02-01 | 8817           | 8920       | -1.2           |
| 2024-03-01 | 9812           | 8817       | 11.3           |
| 2024-04-01 | 9434           | 9812       | -3.9           |
| 2024-05-01 | 10358          | 9434       | 9.8            |
| 2024-06-01 | 10708          | 10358      | 3.4            |
| 2024-07-01 | 10676          | 10708      | -0.3           |
| 2024-08-01 | 11052          | 10676      | 3.5            |
| 2024-09-01 | 11985          | 11052      | 8.4            |
| 2024-10-01 | 11656          | 11985      | -2.7           |
| 2024-11-01 | 11790          | 11656      | 1.1            |
| 2024-12-01 | 17616          | 11790      | 49.4           |


---

## Exercise 9: "Do our premium customers actually spend more?"

### Purchases per customer by segment

```sql
SELECT
    customer.segment,
    COUNT(DISTINCT customer.id) AS customers,
    COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS total_purchases,
    ROUND(
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END)::DECIMAL
        / NULLIF(COUNT(DISTINCT customer.id), 0),
        2
    ) AS purchases_per_customer
FROM retaildb.main.dim_customer customer
LEFT JOIN retaildb.main.fact_customer_action actions ON customer.id = actions.customer_id
WHERE customer.valid_to IS NULL
GROUP BY customer.segment
ORDER BY purchases_per_customer DESC;
```

| segment    | customers | total_purchases | purchases_per_customer |
|------------|-----------|-----------------|------------------------|
| premium    | 1363      | 2252            | 1.65                   |
| mainstream | 4570      | 3535            | 0.77                   |
| budget     | 3141      | 1394            | 0.44                   |


### With revenue per customer

```sql
SELECT
    customer.segment,
    COUNT(DISTINCT customer.id) AS customers,
    COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS purchases,
    ROUND(
        SUM(CASE WHEN actions.action_type = 'purchase' THEN product.price * actions.quantity ELSE 0 END)::DECIMAL
        / NULLIF(COUNT(DISTINCT customer.id), 0),
        2
    ) AS revenue_per_customer
FROM retaildb.main.dim_customer customer
LEFT JOIN retaildb.main.fact_customer_action actions ON customer.id = actions.customer_id
LEFT JOIN retaildb.main.dim_product product ON actions.product_id = product.id
WHERE customer.valid_to IS NULL
GROUP BY customer.segment
ORDER BY revenue_per_customer DESC;
```

| segment    | customers | purchases | revenue_per_customer |
|------------|-----------|-----------|----------------------|
| premium    | 1363      | 2252      | 464.27               |
| mainstream | 4570      | 3535      | 213.39               |
| budget     | 3141      | 1394      | 133.83               |


---

## Exercise 10: "When should we staff up customer support?"

### Hourly breakdown

```sql
SELECT
    EXTRACT(HOUR FROM timestamp)::INT AS hour,
    COUNT(*) AS total_actions,
    ROUND(COUNT(*) / COUNT(DISTINCT timestamp::DATE)::DECIMAL, 1) AS avg_actions_per_day
FROM retaildb.main.fact_customer_action
GROUP BY hour
ORDER BY hour;
```

| hour | total_actions | avg_actions_per_day |
|------|---------------|---------------------|
| 6    | 7373          | 9.1                 |
| 7    | 6395          | 8.3                 |
| 8    | 6911          | 8.9                 |
| 9    | 16084         | 17.2                |
| 10   | 16633         | 17.8                |
| 11   | 17269         | 18.1                |
| 12   | 11279         | 12.4                |
| 13   | 11105         | 12.4                |
| 14   | 14030         | 15.4                |
| 15   | 14485         | 15.6                |
| 16   | 14929         | 15.9                |
| 17   | 20000         | 20.7                |
| 18   | 20647         | 21.4                |
| 19   | 20156         | 20.7                |
| 20   | 20291         | 20.9                |
| 21   | 13175         | 14.5                |
| 22   | 11856         | 13.3                |


### Hour x Day-of-week cross-tab

```sql
WITH hourly_daily AS (
    SELECT
        timestamp::DATE AS day,
        EXTRACT(HOUR FROM timestamp)::INT AS hour,
        CASE WHEN EXTRACT(DOW FROM timestamp) IN (0, 6) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
        COUNT(*) AS actions
    FROM retaildb.main.fact_customer_action
    GROUP BY day, hour, day_type
)
SELECT
    hour,
    day_type,
    ROUND(AVG(actions), 1) AS avg_actions
FROM hourly_daily
GROUP BY hour, day_type
ORDER BY hour, day_type;
```

| hour | day_type | avg_actions |
|------|----------|-------------|
| 6    | Weekday  | 8.2         |
| 6    | Weekend  | 11          |
| 7    | Weekday  | 7.6         |
| 7    | Weekend  | 9.7         |
| 8    | Weekday  | 8.2         |
| 8    | Weekend  | 10.5        |
| 9    | Weekday  | 15.3        |
| 9    | Weekend  | 21.8        |
| 10   | Weekday  | 15.9        |
| 10   | Weekend  | 22.4        |
| 11   | Weekday  | 15.9        |
| 11   | Weekend  | 23.4        |
| 12   | Weekday  | 11.3        |
| 12   | Weekend  | 15          |
| 13   | Weekday  | 11          |
| 13   | Weekend  | 15.8        |
| 14   | Weekday  | 13.6        |
| 14   | Weekend  | 19.6        |
| 15   | Weekday  | 13.9        |
| 15   | Weekend  | 19.7        |
| 16   | Weekday  | 14.3        |
| 16   | Weekend  | 19.7        |
| 17   | Weekday  | 18.2        |
| 17   | Weekend  | 27          |
| 18   | Weekday  | 19          |
| 18   | Weekend  | 27.3        |
| 19   | Weekday  | 18.4        |
| 19   | Weekend  | 26.4        |
| 20   | Weekday  | 18.6        |
| 20   | Weekend  | 26.6        |
| 21   | Weekday  | 13.2        |
| 21   | Weekend  | 17.4        |
| 22   | Weekday  | 11.8        |
| 22   | Weekend  | 16.7        |


---

## Exercise 11: "Who are our most valuable customers beyond the VIP list?"

### Sorting by multiple criteria

```sql
WITH customer_stats AS (
    SELECT
        customer.id,
        customer.name,
        customer.segment,
        customer.tier,
        customer.income,
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT actions.session_id) AS visits
    FROM retaildb.main.dim_customer customer
    INNER JOIN retaildb.main.fact_customer_action actions ON customer.id = actions.customer_id
    WHERE customer.valid_to IS NULL
    GROUP BY customer.id, customer.name, customer.segment, customer.tier, customer.income
)
SELECT
    id,
    name,
    segment,
    tier,
    purchases,
    visits,
    income
FROM customer_stats
WHERE tier != 'vip'
ORDER BY purchases DESC, visits DESC
LIMIT 25;
```

| id          | name                  | segment    | tier    | purchases | visits | income      |
|-------------|-----------------------|------------|---------|-----------|--------|-------------|
| CUST_004773 | Sheila Martin         | mainstream | regular | 38        | 88     | 45384.8325  |
| CUST_002940 | Michael Logan         | premium    | regular | 37        | 95     | 71848.8174  |
| CUST_001504 | Thomas Stephens       | premium    | regular | 36        | 115    | 17833.3072  |
| CUST_003882 | Jamie Graham          | premium    | regular | 34        | 94     | 21394.1792  |
| CUST_004498 | Mallory Lynch         | premium    | regular | 33        | 109    | 12428.1574  |
| CUST_003828 | Kyle Murphy           | budget     | regular | 32        | 166    | 33726.7862  |
| CUST_006053 | Jennifer Barnes       | mainstream | regular | 32        | 77     | 27813.7752  |
| CUST_003688 | Samantha Cole         | premium    | regular | 31        | 131    | 47502.6143  |
| CUST_000144 | Sara Smith            | mainstream | regular | 30        | 197    | 25820.6039  |
| CUST_001416 | Dr Russell Harris     | mainstream | regular | 30        | 148    | 95331.0421  |
| CUST_001678 | Stephen Keller        | premium    | regular | 30        | 128    | 37419.874   |
| CUST_002622 | Louis Long            | mainstream | regular | 30        | 127    | 42130.8566  |
| CUST_000597 | Sheila Andrews        | budget     | regular | 29        | 296    | 63658.1968  |
| CUST_002568 | Steven Williams       | mainstream | regular | 29        | 135    | 62823.441   |
| CUST_000135 | Dr Marc Marshall      | mainstream | regular | 28        | 210    | 67270.0097  |
| CUST_001247 | Germán Aguilar Aranda | mainstream | regular | 28        | 98     | 30390.2245  |
| CUST_000755 | Lic. Perla Domínguez  | budget     | regular | 27        | 302    | 30120.5319  |
| CUST_001110 | Timothy Evans         | mainstream | regular | 27        | 241    | 58332.4507  |
| CUST_004352 | Graeme Morley-Owens   | mainstream | regular | 27        | 125    | 35131.0414  |
| CUST_002871 | John Zhang            | mainstream | regular | 27        | 115    | 147199.4191 |
| CUST_001472 | Jennifer Velez        | premium    | regular | 27        | 101    | 26174.5554  |
| CUST_005208 | Alicia Castaneda      | premium    | regular | 27        | 98     | 45668.2081  |
| CUST_000779 | Anne Rose             | premium    | regular | 27        | 88     | 29868.6103  |
| CUST_003012 | Melissa Robertson     | premium    | regular | 27        | 85     | 21891.9057  |
| CUST_000302 | John Baker            | budget     | regular | 26        | 318    | 73423.8459  |


---

## Exercise 12: "Are customers from paid search worth the money?"

```sql
WITH channel_metrics AS (
    SELECT
        customer.acquisition_source AS channel,
        COUNT(DISTINCT customer.id) AS customers,
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'purchase' THEN customer.id END) AS buyers,
        COUNT(DISTINCT actions.session_id) AS total_sessions
    FROM retaildb.main.dim_customer customer
    LEFT JOIN retaildb.main.fact_customer_action actions ON customer.id = actions.customer_id
    WHERE customer.valid_to IS NULL
    GROUP BY customer.acquisition_source
)
SELECT
    channel,
    customers,
    purchases,
    ROUND(100.0 * buyers / NULLIF(customers, 0), 1) AS buyer_pct,
    ROUND(purchases::DECIMAL / NULLIF(customers, 0), 2) AS purchases_per_customer,
    ROUND(total_sessions::DECIMAL / NULLIF(customers, 0), 1) AS sessions_per_customer
FROM channel_metrics
ORDER BY purchases_per_customer DESC;
```

| channel     | customers | purchases | buyer_pct | purchases_per_customer | sessions_per_customer |
|-------------|-----------|-----------|-----------|------------------------|-----------------------|
| organic     | 3638      | 3130      | 7.7       | 0.86                   | 6.2                   |
| paid_search | 2718      | 2136      | 6.8       | 0.79                   | 6.6                   |
| social      | 1807      | 1331      | 7.4       | 0.74                   | 6.1                   |
| referral    | 911       | 584       | 7.1       | 0.64                   | 5.7                   |


---

## Exercise 13: "Customers browse a lot but don't seem to buy. What's going on?"

### Funnel by segment

```sql
WITH funnel AS (
    SELECT
        customer.segment,
        COUNT(DISTINCT customer.id) AS total_customers,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'product_view' THEN customer.id END) AS viewers,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'add_to_cart' THEN customer.id END) AS carted,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'purchase' THEN customer.id END) AS purchasers
    FROM retaildb.main.dim_customer customer
    LEFT JOIN retaildb.main.fact_customer_action actions ON customer.id = actions.customer_id
    WHERE customer.valid_to IS NULL
    GROUP BY customer.segment
)
SELECT
    segment,
    total_customers,
    viewers,
    carted,
    purchasers,
    ROUND(100.0 * viewers / NULLIF(total_customers, 0), 1) AS view_pct,
    ROUND(100.0 * carted / NULLIF(viewers, 0), 1) AS view_to_cart_pct,
    ROUND(100.0 * purchasers / NULLIF(carted, 0), 1) AS cart_to_purchase_pct
FROM funnel
ORDER BY segment;
```

| segment    | total_customers | viewers | carted | purchasers | view_pct | view_to_cart_pct | cart_to_purchase_pct |
|------------|-----------------|---------|--------|------------|----------|------------------|----------------------|
| budget     | 3141            | 2551    | 2577   | 150        | 81.2     | 101              | 5.8                  |
| mainstream | 4570            | 3664    | 3737   | 334        | 80.2     | 102              | 8.9                  |
| premium    | 1363            | 1113    | 1128   | 179        | 81.7     | 101.3            | 15.9                 |


---

## Exercise 14: "Did the spring sale actually work?"

```sql
WITH periods AS (
    SELECT
        CASE
            WHEN timestamp::DATE BETWEEN '2024-03-08' AND '2024-03-14' THEN 'Week Before'
            WHEN timestamp::DATE BETWEEN '2024-03-15' AND '2024-03-17' THEN 'Sale Period'
            WHEN timestamp::DATE BETWEEN '2024-03-18' AND '2024-03-24' THEN 'Week After'
        END AS period,
        action_type,
        timestamp::DATE AS day
    FROM retaildb.main.fact_customer_action
    WHERE timestamp::DATE BETWEEN '2024-03-08' AND '2024-03-24'
)
SELECT
    period,
    COUNT(*) AS total_actions,
    ROUND(COUNT(*) / COUNT(DISTINCT day)::DECIMAL, 1) AS avg_daily_actions,
    COUNT(CASE WHEN action_type = 'add_to_cart' THEN 1 END) AS cart_adds,
    COUNT(CASE WHEN action_type = 'purchase' THEN 1 END) AS purchases,
    ROUND(
        COUNT(CASE WHEN action_type = 'add_to_cart' THEN 1 END)::DECIMAL
        / NULLIF(COUNT(DISTINCT day), 0),
        1
    ) AS avg_daily_cart_adds
FROM periods
WHERE period IS NOT NULL
GROUP BY period
ORDER BY
    CASE period
        WHEN 'Week Before' THEN 1
        WHEN 'Sale Period' THEN 2
        WHEN 'Week After' THEN 3
    END;
```

| period      | total_actions | avg_daily_actions | cart_adds | purchases | avg_daily_cart_adds |
|-------------|---------------|-------------------|-----------|-----------|---------------------|
| Week Before | 2320          | 331.4             | 782       | 74        | 111.7               |
| Sale Period | 881           | 293.7             | 271       | 37        | 90.3                |
| Week After  | 2336          | 333.7             | 740       | 83        | 105.7               |


---

## Exercise 15: "Which customers should we worry about?"

```sql
WITH customer_activity AS (
    SELECT
        customer.id,
        customer.name,
        customer.segment,
        customer.income,
        COUNT(*) AS total_actions,
        MAX(actions.timestamp) AS last_activity,
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT actions.session_id) AS sessions
    FROM retaildb.main.dim_customer customer
    INNER JOIN retaildb.main.fact_customer_action actions ON customer.id = actions.customer_id
    WHERE customer.valid_to IS NULL AND customer.active = true
    GROUP BY customer.id, customer.name, customer.segment, customer.income
),
risk_scored AS (
    SELECT
        *,
        DATE_DIFF('day', last_activity::DATE, '2024-12-31') AS days_inactive,
        CASE WHEN total_actions > 10 AND purchases = 0 THEN 1 ELSE 0 END AS engaged_non_buyer
    FROM customer_activity
)
SELECT
    id,
    name,
    segment,
    income,
    total_actions,
    purchases,
    sessions,
    days_inactive,
    engaged_non_buyer
FROM risk_scored
WHERE days_inactive > 30 OR engaged_non_buyer = 1
ORDER BY engaged_non_buyer DESC, total_actions DESC, days_inactive DESC
LIMIT 50;
```

| id          | name                      | segment    | income      | total_actions | purchases | sessions | days_inactive | engaged_non_buyer |
|-------------|---------------------------|------------|-------------|---------------|-----------|----------|---------------|-------------------|
| CUST_005066 | Kirk Carrillo             | mainstream | 42269.8411  | 20            | 0         | 1        | 376           | 1                 |
| CUST_005190 | Manuel Pacheco Ulloa      | mainstream | 82536.3419  | 17            | 0         | 1        | 363           | 1                 |
| CUST_006070 | Andrés Jaimes Mendoza     | budget     | 28003.2413  | 17            | 0         | 1        | 255           | 1                 |
| CUST_007560 | Jeffrey Price             | mainstream | 128925.5623 | 17            | 0         | 1        | 106           | 1                 |
| CUST_008268 | Mrs Kirsty Anderson       | budget     | 22340.8263  | 17            | 0         | 1        | 39            | 1                 |
| CUST_000047 | Ing. Marcela Perea        | mainstream | 64599.857   | 16            | 0         | 1        | 1029          | 1                 |
| CUST_000154 | Marisol Ballesteros       | budget     | 26611.925   | 16            | 0         | 1        | 1011          | 1                 |
| CUST_000529 | James Butler              | premium    | 55832.4782  | 16            | 0         | 1        | 943           | 1                 |
| CUST_002619 | Justin Thompson Jr.       | budget     | 22300.6033  | 16            | 0         | 1        | 655           | 1                 |
| CUST_003361 | Geoffrey Manning          | premium    | 46381.0982  | 16            | 0         | 1        | 551           | 1                 |
| CUST_003472 | Lauren Arnold             | mainstream | 45076.7137  | 16            | 0         | 1        | 534           | 1                 |
| CUST_004921 | Raymond Higgins           | premium    | 52419.2948  | 16            | 0         | 1        | 384           | 1                 |
| CUST_000283 | Curtis Branch             | mainstream | 70774.2843  | 15            | 0         | 1        | 989           | 1                 |
| CUST_001232 | Phillip Walker            | budget     | 45161.9465  | 15            | 0         | 1        | 835           | 1                 |
| CUST_001236 | Christopher Mcconnell     | mainstream | 60908.8983  | 15            | 0         | 1        | 834           | 1                 |
| CUST_004569 | Susana Lucas Nava         | mainstream | 28801.4706  | 15            | 0         | 1        | 404           | 1                 |
| CUST_005480 | Mtro. Camilo Tórrez       | mainstream | 54665.7332  | 15            | 0         | 1        | 322           | 1                 |
| CUST_006634 | Ms Maureen Harris         | budget     | 91580.9327  | 15            | 0         | 1        | 201           | 1                 |
| CUST_006916 | Alonso Reina Mata de León | budget     | 31614.3561  | 15            | 0         | 1        | 163           | 1                 |
| CUST_006998 | Andre Davis               | budget     | 213970.6884 | 15            | 0         | 1        | 155           | 1                 |
| CUST_007001 | Matthew Oliver            | budget     | 12686.5614  | 15            | 0         | 1        | 154           | 1                 |
| CUST_008460 | Troy Anderson             | mainstream | 17771.7556  | 15            | 0         | 1        | 30            | 1                 |
| CUST_001297 | Ryan Ferguson             | budget     | 50333.3066  | 14            | 0         | 1        | 825           | 1                 |
| CUST_001348 | Zachary Anderson          | mainstream | 180830.7812 | 14            | 0         | 1        | 816           | 1                 |
| CUST_002410 | Mayte Cabán Barreto       | mainstream | 38697.8196  | 14            | 0         | 1        | 681           | 1                 |
| CUST_004529 | Teresa Lester             | mainstream | 14265.8361  | 14            | 0         | 1        | 409           | 1                 |
| CUST_004945 | Heather Johnson           | mainstream | 49264.2369  | 14            | 0         | 1        | 382           | 1                 |
| CUST_005482 | Anthony Newton            | budget     | 131649.155  | 14            | 0         | 1        | 322           | 1                 |
| CUST_006765 | Julian Andrews            | budget     | 43555.5037  | 14            | 0         | 1        | 184           | 1                 |
| CUST_007073 | Richard Ruiz              | budget     | 28640.3023  | 14            | 0         | 1        | 146           | 1                 |
| CUST_007505 | Dylan Sanchez             | mainstream | 68249.9524  | 14            | 0         | 1        | 110           | 1                 |
| CUST_008204 | William Torres            | budget     | 57905.66    | 14            | 0         | 1        | 43            | 1                 |
| CUST_008463 | Kirsty Cox-Edwards        | mainstream | 55171.743   | 14            | 0         | 1        | 30            | 1                 |
| CUST_008679 | Anthony Rodriguez         | budget     | 25225.1834  | 14            | 0         | 1        | 19            | 1                 |
| CUST_008704 | Donald Lewis              | premium    | 82651.0832  | 14            | 0         | 1        | 18            | 1                 |
| CUST_008839 | Donald Hudson             | mainstream | 43315.4131  | 14            | 0         | 1        | 12            | 1                 |
| CUST_000328 | Christopher Hill          | budget     | 38137.1717  | 13            | 0         | 1        | 980           | 1                 |
| CUST_000676 | Dan Robinson              | mainstream | 26947.6833  | 13            | 0         | 1        | 914           | 1                 |
| CUST_000842 | Julie Mitchell            | budget     | 48063.9176  | 13            | 0         | 1        | 882           | 1                 |
| CUST_000920 | Gary Wheeler              | premium    | 46811.1797  | 13            | 0         | 1        | 868           | 1                 |
| CUST_001363 | Travis Odom               | premium    | 27977.1935  | 13            | 0         | 1        | 815           | 1                 |
| CUST_002294 | James Evans               | mainstream | 173512.5342 | 13            | 0         | 1        | 698           | 1                 |
| CUST_002616 | Austin Alvarado           | mainstream | 26710.3412  | 13            | 0         | 1        | 655           | 1                 |
| CUST_003415 | Dawn Mcdaniel             | mainstream | 34169.1868  | 13            | 0         | 1        | 543           | 1                 |
| CUST_003617 | Mrs Frances Fox           | budget     | 34603.9472  | 13            | 0         | 1        | 509           | 1                 |
| CUST_004070 | Kevin Johnson             | mainstream | 58015.4078  | 13            | 0         | 1        | 464           | 1                 |
| CUST_004264 | Cristobal Villalobos      | premium    | 49678.7237  | 13            | 0         | 1        | 440           | 1                 |
| CUST_004797 | Amanda Woods              | mainstream | 118087.0612 | 13            | 0         | 1        | 392           | 1                 |
| CUST_005503 | Larry Smith               | budget     | 80351.9193  | 13            | 0         | 1        | 320           | 1                 |
| CUST_005525 | Lacey Gamble              | mainstream | 121643.802  | 13            | 0         | 1        | 317           | 1                 |


---

## Exercise 16: "Build me something that shows how the business is doing."

### Monthly executive dashboard

```sql
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', actions.timestamp)::DATE AS month,
        COUNT(DISTINCT actions.customer_id) AS active_customers,
        COUNT(CASE WHEN actions.action_type = 'visit' THEN 1 END) AS visits,
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'purchase' THEN actions.customer_id END) AS buyers
    FROM retaildb.main.fact_customer_action actions
    WHERE actions.timestamp < '2025-01-01'
    GROUP BY month
),
with_trends AS (
    SELECT
        month,
        active_customers,
        visits,
        purchases,
        buyers,
        ROUND(100.0 * buyers / NULLIF(active_customers, 0), 1) AS conversion_rate,
        ROUND(100.0 * (purchases - LAG(purchases) OVER (ORDER BY month))
            / NULLIF(LAG(purchases) OVER (ORDER BY month), 0), 1) AS purchase_growth_pct,
        ROUND(100.0 * (active_customers - LAG(active_customers) OVER (ORDER BY month))
            / NULLIF(LAG(active_customers) OVER (ORDER BY month), 0), 1) AS customer_growth_pct
    FROM monthly
)
SELECT
    month,
    active_customers,
    visits,
    purchases,
    conversion_rate AS conversion_pct,
    purchase_growth_pct AS mom_purchase_growth,
    customer_growth_pct AS mom_customer_growth
FROM with_trends
ORDER BY month;
```

| month      | active_customers | visits | purchases | conversion_pct | mom_purchase_growth | mom_customer_growth |
|------------|------------------|--------|-----------|----------------|---------------------|---------------------|
| 2022-03-01 | 187              | 201    | 26        | 7.5            | NULL                | NULL                |
| 2022-04-01 | 171              | 256    | 33        | 11.1           | 26.9                | -8.6                |
| 2022-05-01 | 194              | 356    | 41        | 9.8            | 24.2                | 13.5                |
| 2022-06-01 | 182              | 423    | 38        | 12.1           | -7.3                | -6.2                |
| 2022-07-01 | 198              | 518    | 62        | 15.2           | 63.2                | 8.8                 |
| 2022-08-01 | 278              | 649    | 76        | 14             | 22.6                | 40.4                |
| 2022-09-01 | 297              | 726    | 90        | 14.8           | 18.4                | 6.8                 |
| 2022-10-01 | 262              | 804    | 111       | 20.2           | 23.3                | -11.8               |
| 2022-11-01 | 377              | 929    | 123       | 14.6           | 10.8                | 43.9                |
| 2022-12-01 | 422              | 1232   | 128       | 14             | 4.1                 | 11.9                |
| 2023-01-01 | 277              | 1147   | 137       | 23.1           | 7                   | -34.4               |
| 2023-02-01 | 298              | 1120   | 116       | 21.1           | -15.3               | 7.6                 |
| 2023-03-01 | 390              | 1328   | 179       | 22.6           | 54.3                | 30.9                |
| 2023-04-01 | 346              | 1374   | 209       | 26.9           | 16.8                | -11.3               |
| 2023-05-01 | 365              | 1487   | 219       | 25.8           | 4.8                 | 5.5                 |
| 2023-06-01 | 377              | 1575   | 200       | 25.7           | -8.7                | 3.3                 |
| 2023-07-01 | 357              | 1640   | 227       | 30             | 13.5                | -5.3                |
| 2023-08-01 | 431              | 1765   | 189       | 22             | -16.7               | 20.7                |
| 2023-09-01 | 482              | 1933   | 211       | 23.2           | 11.6                | 11.8                |
| 2023-10-01 | 456              | 1927   | 280       | 27.2           | 32.7                | -5.4                |
| 2023-11-01 | 533              | 2070   | 275       | 22.9           | -1.8                | 16.9                |
| 2023-12-01 | 671              | 2352   | 289       | 20.6           | 5.1                 | 25.9                |
| 2024-01-01 | 417              | 2076   | 262       | 30.5           | -9.3                | -37.9               |
| 2024-02-01 | 464              | 2075   | 271       | 29.3           | 3.4                 | 11.3                |
| 2024-03-01 | 524              | 2302   | 293       | 25             | 8.1                 | 12.9                |
| 2024-04-01 | 517              | 2269   | 256       | 26.1           | -12.6               | -1.3                |
| 2024-05-01 | 561              | 2450   | 282       | 23.9           | 10.2                | 8.5                 |
| 2024-06-01 | 531              | 2494   | 318       | 29.2           | 12.8                | -5.3                |
| 2024-07-01 | 512              | 2506   | 299       | 29.3           | -6                  | -3.6                |
| 2024-08-01 | 596              | 2580   | 320       | 25.3           | 7                   | 16.4                |
| 2024-09-01 | 646              | 2782   | 380       | 26.5           | 18.8                | 8.4                 |
| 2024-10-01 | 595              | 2756   | 360       | 28.7           | -5.3                | -7.9                |
| 2024-11-01 | 692              | 2757   | 336       | 25.4           | -6.7                | 16.3                |
| 2024-12-01 | 934              | 4139   | 545       | 25.7           | 62.2                | 35                  |


---

## Exercise 17: "Black Friday was supposed to be our biggest day. What went wrong?"

### Step 1: Confirm the claim -- was Black Friday really bad?

```sql
WITH daily AS (
    SELECT timestamp::DATE AS day, COUNT(*) AS activity
    FROM retaildb.main.fact_customer_action
    GROUP BY day
),
baseline AS (
    SELECT AVG(activity) AS avg_daily
    FROM daily
    WHERE day BETWEEN '2024-11-15' AND '2024-11-28'
)
SELECT
    daily.day,
    daily.activity,
    ROUND(daily.activity / baseline.avg_daily, 2) AS vs_baseline
FROM daily CROSS JOIN baseline
WHERE daily.day BETWEEN '2024-11-25' AND '2024-12-07'
ORDER BY daily.day;
```

| day        | activity | vs_baseline |
|------------|----------|-------------|
| 2024-11-25 | 362      | 0.87        |
| 2024-11-26 | 305      | 0.74        |
| 2024-11-27 | 324      | 0.78        |
| 2024-11-28 | 377      | 0.91        |
| 2024-11-29 | 222      | 0.54        |
| 2024-11-30 | 565      | 1.36        |
| 2024-12-01 | 622      | 1.5         |
| 2024-12-02 | 649      | 1.57        |
| 2024-12-03 | 637      | 1.54        |
| 2024-12-04 | 638      | 1.54        |
| 2024-12-05 | 458      | 1.11        |
| 2024-12-06 | 577      | 1.39        |
| 2024-12-07 | 512      | 1.24        |


### Step 2: Discover the infrastructure table

```sql
SELECT * FROM retaildb.main.dim_infrastructure ORDER BY valid_from;
```

| id         | status   | primary_ip   | domain                   | error_rate | valid_from          | valid_to            |
|------------|----------|--------------|--------------------------|------------|---------------------|---------------------|
| INFRA_0001 | healthy  | 10.0.1.100   | techmart-electronics.com | 0.02       | 2022-03-01 00:00:00 | 2024-03-15 00:00:00 |
| INFRA_0002 | healthy  | 19.48.39.204 | murray.com               | 0.02       | 2022-03-01 00:00:00 | NULL                |
| INFRA_0001 | degraded | 10.0.1.100   | techmart-electronics.com | 0.35       | 2024-03-15 00:00:00 | 2024-03-16 00:00:00 |
| INFRA_0001 | healthy  | 10.0.1.100   | techmart-electronics.com | 0.02       | 2024-03-16 00:00:00 | 2024-08-22 00:00:00 |
| INFRA_0001 | degraded | 10.0.1.100   | techmart-electronics.com | 0.4        | 2024-08-22 00:00:00 | 2024-08-23 00:00:00 |
| INFRA_0001 | healthy  | 10.0.1.100   | techmart-electronics.com | 0.02       | 2024-08-23 00:00:00 | 2024-11-29 00:00:00 |
| INFRA_0001 | degraded | 10.0.1.100   | techmart-electronics.com | 0.25       | 2024-11-29 00:00:00 | 2024-11-30 00:00:00 |
| INFRA_0001 | healthy  | 10.0.1.100   | techmart-electronics.com | 0.02       | 2024-11-30 00:00:00 | NULL                |


### Step 3: Connect the outage to the dip

```sql
SELECT
    id,
    status,
    error_rate,
    valid_from::DATE AS started,
    valid_to::DATE AS ended
FROM retaildb.main.dim_infrastructure
WHERE id = 'INFRA_0001'
ORDER BY valid_from;
```

| id         | status   | error_rate | started    | ended      |
|------------|----------|------------|------------|------------|
| INFRA_0001 | healthy  | 0.02       | 2022-03-01 | 2024-03-15 |
| INFRA_0001 | degraded | 0.35       | 2024-03-15 | 2024-03-16 |
| INFRA_0001 | healthy  | 0.02       | 2024-03-16 | 2024-08-22 |
| INFRA_0001 | degraded | 0.4        | 2024-08-22 | 2024-08-23 |
| INFRA_0001 | healthy  | 0.02       | 2024-08-23 | 2024-11-29 |
| INFRA_0001 | degraded | 0.25       | 2024-11-29 | 2024-11-30 |
| INFRA_0001 | healthy  | 0.02       | 2024-11-30 | NULL       |


### Step 4 (thorough answer): Quantify all outage impacts

```sql
WITH outages AS (
    SELECT
        valid_from::DATE AS outage_date,
        valid_to::DATE AS recovery_date
    FROM retaildb.main.dim_infrastructure
    WHERE id = 'INFRA_0001' AND status = 'degraded'
),
daily AS (
    SELECT timestamp::DATE AS day, COUNT(*) AS activity
    FROM retaildb.main.fact_customer_action
    GROUP BY day
)
SELECT
    outage.outage_date,
    daily_during.activity AS outage_day_activity,
    daily_before.activity AS day_before_activity,
    daily_after.activity AS day_after_activity,
    ROUND(100.0 * daily_during.activity / daily_before.activity, 1) AS pct_of_prior_day
FROM outages outage
LEFT JOIN daily daily_during ON daily_during.day = outage.outage_date
LEFT JOIN daily daily_before ON daily_before.day = outage.outage_date - INTERVAL '1 day'
LEFT JOIN daily daily_after ON daily_after.day = outage.recovery_date
ORDER BY outage.outage_date;
```

| outage_date | outage_day_activity | day_before_activity | day_after_activity | pct_of_prior_day |
|-------------|---------------------|---------------------|--------------------|------------------|
| 2024-03-15  | 30                  | 366                 | 450                | 8.2              |
| 2024-08-22  | 16                  | 345                 | 296                | 4.6              |
| 2024-11-29  | 222                 | 377                 | 565                | 58.9             |


---

## Exercise 18: "Do bigger carts convert better?"

### Compare cart quantity between converted and abandoned sessions

```sql
WITH session_carts AS (
    SELECT
        session_id,
        SUM(CASE WHEN action_type = 'add_to_cart' THEN quantity ELSE 0 END) AS cart_quantity,
        MAX(CASE WHEN action_type = 'purchase' THEN 1 ELSE 0 END) AS converted
    FROM retaildb.main.fact_customer_action
    GROUP BY session_id
    HAVING SUM(CASE WHEN action_type = 'add_to_cart' THEN 1 ELSE 0 END) > 0
)
SELECT
    CASE WHEN converted = 1 THEN 'Converted' ELSE 'Abandoned' END AS outcome,
    COUNT(*) AS sessions,
    ROUND(AVG(cart_quantity), 2) AS avg_cart_quantity
FROM session_carts
GROUP BY converted
ORDER BY converted DESC;
```

| outcome   | sessions | avg_cart_quantity |
|-----------|----------|-------------------|
| Converted | 4220     | 2.92              |
| Abandoned | 42739    | 2.9               |


### Conversion rate by cart size bucket

```sql
WITH session_carts AS (
    SELECT
        session_id,
        SUM(CASE WHEN action_type = 'add_to_cart' THEN quantity ELSE 0 END) AS cart_quantity,
        MAX(CASE WHEN action_type = 'purchase' THEN 1 ELSE 0 END) AS converted
    FROM retaildb.main.fact_customer_action
    GROUP BY session_id
    HAVING SUM(CASE WHEN action_type = 'add_to_cart' THEN 1 ELSE 0 END) > 0
)
SELECT
    CASE
        WHEN cart_quantity = 1 THEN '1 item'
        WHEN cart_quantity BETWEEN 2 AND 3 THEN '2-3 items'
        WHEN cart_quantity BETWEEN 4 AND 5 THEN '4-5 items'
        ELSE '6+ items'
    END AS cart_size,
    COUNT(*) AS sessions,
    SUM(converted) AS converted,
    ROUND(100.0 * SUM(converted) / COUNT(*), 1) AS conversion_pct
FROM session_carts
GROUP BY cart_size
ORDER BY cart_size;
```

| cart_size | sessions | converted | conversion_pct |
|-----------|----------|-----------|----------------|
| 1 item    | 15515    | 1385      | 8.9            |
| 2-3 items | 17958    | 1618      | 9              |
| 4-5 items | 8095     | 730       | 9              |
| 6+ items  | 5391     | 487       | 9              |


---

## Exercise 19: "What's our average order value, and is it changing?"

### Monthly AOV with month-over-month change

```sql
WITH purchase_revenue AS (
    SELECT
        session_id,
        DATE_TRUNC('month', timestamp)::DATE AS month,
        SUM(product.price * actions.quantity * (1 - actions.discount_pct)) AS order_value
    FROM retaildb.main.fact_customer_action actions
    INNER JOIN retaildb.main.dim_product product ON actions.product_id = product.id
    WHERE actions.action_type = 'purchase'
    GROUP BY session_id, month
),
monthly_aov AS (
    SELECT
        month,
        COUNT(*) AS orders,
        ROUND(AVG(order_value), 2) AS avg_order_value,
        ROUND(SUM(order_value), 2) AS total_revenue
    FROM purchase_revenue
    GROUP BY month
)
SELECT
    month,
    orders,
    avg_order_value,
    total_revenue,
    ROUND(100.0 * (avg_order_value - LAG(avg_order_value) OVER (ORDER BY month))
        / NULLIF(LAG(avg_order_value) OVER (ORDER BY month), 0), 1) AS mom_change_pct
FROM monthly_aov
ORDER BY month;
```

| month      | orders | avg_order_value | total_revenue | mom_change_pct |
|------------|--------|-----------------|---------------|----------------|
| 2022-03-01 | 16     | 287.85          | 4605.55       | NULL           |
| 2022-04-01 | 22     | 481.68          | 10596.98      | 67.3           |
| 2022-05-01 | 22     | 366.02          | 8052.33       | -24            |
| 2022-06-01 | 24     | 556.5           | 13355.95      | 52             |
| 2022-07-01 | 36     | 368.94          | 13281.95      | -33.7          |
| 2022-08-01 | 45     | 588.81          | 26496.39      | 59.6           |
| 2022-09-01 | 52     | 397.59          | 20674.68      | -32.5          |
| 2022-10-01 | 63     | 366.49          | 23088.81      | -7.8           |
| 2022-11-01 | 66     | 439.73          | 29021.87      | 20             |
| 2022-12-01 | 73     | 354.88          | 25906.48      | -19.3          |
| 2023-01-01 | 80     | 497.32          | 39785.36      | 40.1           |
| 2023-02-01 | 71     | 307.43          | 21827.27      | -38.2          |
| 2023-03-01 | 111    | 385.42          | 42781.28      | 25.4           |
| 2023-04-01 | 116    | 451.88          | 52418.5       | 17.2           |
| 2023-05-01 | 121    | 551.48          | 66729.62      | 22             |
| 2023-06-01 | 112    | 513.82          | 57548.3       | -6.8           |
| 2023-07-01 | 142    | 458.18          | 65061.65      | -10.8          |
| 2023-08-01 | 117    | 312.72          | 36588.54      | -31.7          |
| 2023-09-01 | 132    | 391.95          | 51736.76      | 25.3           |
| 2023-10-01 | 159    | 513.85          | 81701.96      | 31.1           |
| 2023-11-01 | 159    | 468.04          | 74419.14      | -8.9           |
| 2023-12-01 | 164    | 483.24          | 79251.99      | 3.2            |
| 2024-01-01 | 170    | 384.38          | 65345.24      | -20.5          |
| 2024-02-01 | 163    | 395.84          | 64521.71      | 3              |
| 2024-03-01 | 164    | 415.15          | 68084.4       | 4.9            |
| 2024-04-01 | 150    | 448.03          | 67204.15      | 7.9            |
| 2024-05-01 | 158    | 386.11          | 61004.81      | -13.8          |
| 2024-06-01 | 194    | 473.6           | 91878.7       | 22.7           |
| 2024-07-01 | 178    | 430.02          | 76542.75      | -9.2           |
| 2024-08-01 | 189    | 510.1           | 96409.68      | 18.6           |
| 2024-09-01 | 208    | 451.96          | 94008.53      | -11.4          |
| 2024-10-01 | 218    | 447.25          | 97499.99      | -1             |
| 2024-11-01 | 207    | 527.01          | 109090.89     | 17.8           |
| 2024-12-01 | 318    | 436.37          | 138766.48     | -17.2          |


---

## Exercise 20: "Are discounts actually driving sales?"

### Discount distribution by customer segment

```sql
SELECT
    customer.segment,
    COUNT(*) AS purchases,
    ROUND(AVG(actions.discount_pct) * 100, 1) AS avg_discount_pct,
    ROUND(MIN(actions.discount_pct) * 100, 1) AS min_discount_pct,
    ROUND(MAX(actions.discount_pct) * 100, 1) AS max_discount_pct
FROM retaildb.main.fact_customer_action actions
INNER JOIN retaildb.main.dim_customer customer ON actions.customer_id = customer.id AND customer.valid_to IS NULL
WHERE actions.action_type = 'purchase'
GROUP BY customer.segment
ORDER BY customer.segment;
```

| segment    | purchases | avg_discount_pct | min_discount_pct | max_discount_pct |
|------------|-----------|------------------|------------------|------------------|
| budget     | 1394      | 7.5              | 0                | 15               |
| mainstream | 3535      | 7.5              | 0                | 15               |
| premium    | 2252      | 7.6              | 0                | 15               |


### Discount buckets vs. basket size

```sql
WITH purchase_data AS (
    SELECT
        actions.discount_pct,
        actions.quantity,
        product.price,
        CASE
            WHEN actions.discount_pct < 0.05 THEN '0-5%'
            WHEN actions.discount_pct < 0.10 THEN '5-10%'
            ELSE '10-15%'
        END AS discount_bucket
    FROM retaildb.main.fact_customer_action actions
    INNER JOIN retaildb.main.dim_product product ON actions.product_id = product.id
    WHERE actions.action_type = 'purchase'
)
SELECT
    discount_bucket,
    COUNT(*) AS purchases,
    ROUND(AVG(quantity), 2) AS avg_quantity,
    ROUND(AVG(price * quantity), 2) AS avg_gross_value,
    ROUND(AVG(price * quantity * (1 - discount_pct)), 2) AS avg_net_value
FROM purchase_data
GROUP BY discount_bucket
ORDER BY MIN(discount_pct);
```

| discount_bucket | purchases | avg_quantity | avg_gross_value | avg_net_value |
|-----------------|-----------|--------------|-----------------|---------------|
| 0-5%            | 2112      | 1.7          | 288.51          | 282.14        |
| 5-10%           | 2399      | 1.71         | 272.46          | 253.51        |
| 10-15%          | 2670      | 1.73         | 286.67          | 251.4         |


---

## Exercise 21: "Which products do customers browse together?"

### Category-level co-occurrence (more actionable)

```sql
SELECT
    product1.category AS category_1,
    product2.category AS category_2,
    COUNT(DISTINCT action1.session_id) AS shared_sessions
FROM retaildb.main.fact_customer_action action1
INNER JOIN retaildb.main.fact_customer_action action2
    ON action1.session_id = action2.session_id
    AND action1.product_id <> action2.product_id
INNER JOIN retaildb.main.dim_product product1 ON action1.product_id = product1.id
INNER JOIN retaildb.main.dim_product product2 ON action2.product_id = product2.id
WHERE action1.action_type = 'product_view'
  AND action2.action_type = 'product_view'
  AND product1.category < product2.category
GROUP BY product1.category, product2.category
ORDER BY shared_sessions DESC;
```

| category_1  | category_2  | shared_sessions |
|-------------|-------------|-----------------|
| accessories | smartphones | 5038            |
| accessories | laptops     | 4213            |
| accessories | gaming      | 3628            |
| laptops     | smartphones | 3615            |
| gaming      | smartphones | 3055            |
| accessories | audio       | 3029            |
| audio       | smartphones | 2569            |
| gaming      | laptops     | 2545            |
| audio       | laptops     | 2064            |
| audio       | gaming      | 1938            |
| accessories | tablets     | 1643            |
| smartphones | tablets     | 1341            |
| laptops     | tablets     | 1151            |
| gaming      | tablets     | 972             |
| audio       | tablets     | 789             |


### Product-level co-occurrence

```sql
SELECT
    product1.name AS product_1,
    product2.name AS product_2,
    product1.category AS cat_1,
    product2.category AS cat_2,
    COUNT(DISTINCT action1.session_id) AS shared_sessions
FROM retaildb.main.fact_customer_action action1
INNER JOIN retaildb.main.fact_customer_action action2
    ON action1.session_id = action2.session_id
    AND action1.product_id < action2.product_id
INNER JOIN retaildb.main.dim_product product1 ON action1.product_id = product1.id
INNER JOIN retaildb.main.dim_product product2 ON action2.product_id = product2.id
WHERE action1.action_type = 'product_view'
  AND action2.action_type = 'product_view'
GROUP BY product1.name, product2.name, product1.category, product2.category
ORDER BY shared_sessions DESC
LIMIT 15;
```

| product_1             | product_2             | cat_1       | cat_2       | shared_sessions |
|-----------------------|-----------------------|-------------|-------------|-----------------|
| Classic Soundbar      | Pro Ring              | audio       | accessories | 42              |
| Basic Ring            | Essential Phone Stand | accessories | smartphones | 37              |
| Classic Stream Deck   | Pro Ring              | gaming      | accessories | 36              |
| Classic Stream Deck   | Premium Laptop Sleeve | gaming      | laptops     | 36              |
| Classic Soundbar      | Basic Cooling Pad     | audio       | laptops     | 35              |
| Basic Power Bank      | Premium Laptop Sleeve | smartphones | laptops     | 34              |
| Basic Ring            | Premium Laptop Sleeve | accessories | laptops     | 32              |
| Basic Ring            | Elite Strap           | accessories | accessories | 32              |
| Basic Strap           | Premium Laptop Sleeve | accessories | laptops     | 32              |
| Premium Laptop Sleeve | Pro Ring              | laptops     | accessories | 31              |
| Classic Power Bank    | Essential Phone Stand | smartphones | smartphones | 31              |
| Basic Ring            | Pro Ring              | accessories | accessories | 30              |
| Pro Charging Dock     | Basic Cooling Pad     | smartphones | laptops     | 30              |
| Classic Cable         | Pro Ring              | accessories | accessories | 28              |
| Classic Cable         | Pro Charging Dock     | accessories | smartphones | 28              |


---

## Exercise 22: "Are we keeping customers, or just finding new ones?"

### Cohort retention table

```sql
WITH first_visit AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(timestamp))::DATE AS cohort_month
    FROM retaildb.main.fact_customer_action
    GROUP BY customer_id
),
activity AS (
    SELECT
        first_visit.cohort_month,
        actions.customer_id,
        DATE_DIFF('month',
            first_visit.cohort_month,
            DATE_TRUNC('month', actions.timestamp)::DATE
        ) AS months_since_first
    FROM retaildb.main.fact_customer_action actions
    INNER JOIN first_visit ON actions.customer_id = first_visit.customer_id
)
SELECT
    cohort_month,
    COUNT(DISTINCT CASE WHEN months_since_first = 0 THEN customer_id END) AS month_0,
    COUNT(DISTINCT CASE WHEN months_since_first = 1 THEN customer_id END) AS month_1,
    COUNT(DISTINCT CASE WHEN months_since_first = 3 THEN customer_id END) AS month_3,
    COUNT(DISTINCT CASE WHEN months_since_first = 6 THEN customer_id END) AS month_6,
    COUNT(DISTINCT CASE WHEN months_since_first = 12 THEN customer_id END) AS month_12,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN months_since_first = 1 THEN customer_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN months_since_first = 0 THEN customer_id END), 0),
        1
    ) AS retention_m1_pct
FROM activity
GROUP BY cohort_month
ORDER BY cohort_month;
```

| cohort_month | month_0 | month_1 | month_3 | month_6 | month_12 | retention_m1_pct |
|--------------|---------|---------|---------|---------|----------|------------------|
| 2022-03-01   | 187     | 10      | 10      | 10      | 10       | 5.3              |
| 2022-04-01   | 161     | 11      | 11      | 11      | 11       | 6.8              |
| 2022-05-01   | 173     | 8       | 7       | 7       | 6        | 4.6              |
| 2022-06-01   | 153     | 7       | 7       | 7       | 6        | 4.6              |
| 2022-07-01   | 163     | 15      | 15      | 15      | 13       | 9.2              |
| 2022-08-01   | 228     | 7       | 7       | 7       | 7        | 3.1              |
| 2022-09-01   | 240     | 12      | 12      | 12      | 10       | 5                |
| 2022-10-01   | 193     | 8       | 8       | 8       | 7        | 4.1              |
| 2022-11-01   | 300     | 20      | 20      | 20      | 17       | 6.7              |
| 2022-12-01   | 325     | 15      | 15      | 15      | 12       | 4.6              |
| 2023-01-01   | 165     | 5       | 5       | 5       | 5        | 3                |
| 2023-02-01   | 181     | 7       | 7       | 7       | 6        | 3.9              |
| 2023-03-01   | 267     | 19      | 19      | 19      | 16       | 7.1              |
| 2023-04-01   | 206     | 14      | 14      | 14      | 11       | 6.8              |
| 2023-05-01   | 213     | 13      | 13      | 13      | 10       | 6.1              |
| 2023-06-01   | 219     | 12      | 12      | 12      | 11       | 5.5              |
| 2023-07-01   | 189     | 12      | 12      | 12      | 11       | 6.3              |
| 2023-08-01   | 259     | 14      | 14      | 14      | 13       | 5.4              |
| 2023-09-01   | 301     | 20      | 20      | 20      | 19       | 6.6              |
| 2023-10-01   | 263     | 12      | 12      | 12      | 12       | 4.6              |
| 2023-11-01   | 334     | 18      | 18      | 18      | 16       | 5.4              |
| 2023-12-01   | 462     | 23      | 23      | 23      | 18       | 5                |
| 2024-01-01   | 195     | 15      | 15      | 15      | 0        | 7.7              |
| 2024-02-01   | 237     | 11      | 11      | 11      | 0        | 4.6              |
| 2024-03-01   | 294     | 12      | 12      | 12      | 0        | 4.1              |
| 2024-04-01   | 284     | 28      | 28      | 28      | 0        | 9.9              |
| 2024-05-01   | 308     | 14      | 14      | 14      | 0        | 4.5              |
| 2024-06-01   | 270     | 14      | 14      | 14      | 0        | 5.2              |
| 2024-07-01   | 245     | 12      | 12      | 0       | 0        | 4.9              |
| 2024-08-01   | 329     | 15      | 15      | 0       | 0        | 4.6              |
| 2024-09-01   | 373     | 22      | 21      | 0       | 0        | 5.9              |
| 2024-10-01   | 309     | 16      | 0       | 0       | 0        | 5.2              |
| 2024-11-01   | 408     | 24      | 0       | 0       | 0        | 5.9              |
| 2024-12-01   | 640     | 0       | 0       | 0       | 0        | 0                |


### Aggregate retention curve

```sql
WITH first_visit AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(timestamp))::DATE AS cohort_month
    FROM retaildb.main.fact_customer_action
    GROUP BY customer_id
),
activity AS (
    SELECT
        actions.customer_id,
        DATE_DIFF('month',
            first_visit.cohort_month,
            DATE_TRUNC('month', actions.timestamp)::DATE
        ) AS months_since_first
    FROM retaildb.main.fact_customer_action actions
    INNER JOIN first_visit ON actions.customer_id = first_visit.customer_id
)
SELECT
    months_since_first,
    COUNT(DISTINCT customer_id) AS active_customers,
    ROUND(100.0 * COUNT(DISTINCT customer_id)
        / (SELECT COUNT(DISTINCT customer_id) FROM first_visit),
        1
    ) AS retention_pct
FROM activity
WHERE months_since_first BETWEEN 0 AND 12
GROUP BY months_since_first
ORDER BY months_since_first;
```

| months_since_first | active_customers | retention_pct |
|--------------------|------------------|---------------|
| 0                  | 9074             | 100           |
| 1                  | 465              | 5.1           |
| 2                  | 439              | 4.8           |
| 3                  | 423              | 4.7           |
| 4                  | 402              | 4.4           |
| 5                  | 387              | 4.3           |
| 6                  | 375              | 4.1           |
| 7                  | 357              | 3.9           |
| 8                  | 340              | 3.7           |
| 9                  | 311              | 3.4           |
| 10                 | 296              | 3.3           |
| 11                 | 273              | 3             |
| 12                 | 247              | 2.7           |


---

## Exercise 23: "How much revenue did the Black Friday outage cost us?"

### Step 1: Black Friday revenue by year

```sql
SELECT
    EXTRACT(YEAR FROM actions.timestamp)::INT AS year,
    COUNT(*) AS purchases,
    ROUND(SUM(product.price * actions.quantity * (1 - actions.discount_pct)), 2) AS net_revenue
FROM retaildb.main.fact_customer_action actions
INNER JOIN retaildb.main.dim_product product ON actions.product_id = product.id
WHERE actions.action_type = 'purchase'
  AND (actions.timestamp::DATE = '2022-11-25'   -- Black Friday 2022
    OR actions.timestamp::DATE = '2023-11-24'   -- Black Friday 2023
    OR actions.timestamp::DATE = '2024-11-29')  -- Black Friday 2024
GROUP BY year
ORDER BY year;
```

| year | purchases | net_revenue |
|------|-----------|-------------|
| 2022 | 8         | 1010.38     |
| 2023 | 5         | 752.3       |
| 2024 | 8         | 2254.03     |


### Step 2: Quantify year-over-year growth to project expected 2024

```sql
WITH bf_revenue AS (
    SELECT
        EXTRACT(YEAR FROM actions.timestamp)::INT AS year,
        COUNT(*) AS purchases,
        SUM(product.price * actions.quantity * (1 - actions.discount_pct)) AS net_revenue
    FROM retaildb.main.fact_customer_action actions
    INNER JOIN retaildb.main.dim_product product ON actions.product_id = product.id
    WHERE actions.action_type = 'purchase'
      AND (actions.timestamp::DATE = '2022-11-25'
        OR actions.timestamp::DATE = '2023-11-24'
        OR actions.timestamp::DATE = '2024-11-29')
    GROUP BY year
)
SELECT
    year,
    purchases,
    ROUND(net_revenue, 2) AS net_revenue,
    LAG(net_revenue) OVER (ORDER BY year) AS prev_year_revenue,
    ROUND(100.0 * (net_revenue - LAG(net_revenue) OVER (ORDER BY year))
        / NULLIF(LAG(net_revenue) OVER (ORDER BY year), 0), 1) AS yoy_change_pct
FROM bf_revenue
ORDER BY year;
```

| year | purchases | net_revenue | prev_year_revenue | yoy_change_pct |
|------|-----------|-------------|-------------------|----------------|
| 2022 | 8         | 1010.38     | NULL              | NULL           |
| 2023 | 5         | 752.3       | 1010.38           | -25.5          |
| 2024 | 8         | 2254.03     | 752.3             | 199.6          |


### Step 3: Wider window for a more robust estimate

```sql
WITH bf_dates AS (
    SELECT 2022 AS yr, '2022-11-25'::DATE AS bf_date
    UNION ALL SELECT 2023, '2023-11-24'::DATE
    UNION ALL SELECT 2024, '2024-11-29'::DATE
),
holiday_revenue AS (
    SELECT
        bf_dates.yr AS year,
        actions.timestamp::DATE AS day,
        COUNT(*) AS purchases,
        SUM(product.price * actions.quantity * (1 - actions.discount_pct)) AS net_revenue
    FROM bf_dates
    INNER JOIN retaildb.main.fact_customer_action actions
      ON actions.timestamp::DATE BETWEEN bf_dates.bf_date - INTERVAL '2 days'
                                      AND bf_dates.bf_date + INTERVAL '3 days'
    INNER JOIN retaildb.main.dim_product product ON actions.product_id = product.id
    WHERE actions.action_type = 'purchase'
    GROUP BY bf_dates.yr, actions.timestamp::DATE
)
SELECT
    year,
    COUNT(DISTINCT day) AS days,
    SUM(purchases) AS total_purchases,
    ROUND(SUM(net_revenue), 2) AS total_net_revenue,
    ROUND(AVG(net_revenue), 2) AS avg_daily_revenue
FROM holiday_revenue
GROUP BY year
ORDER BY year;
```

| year | days | total_purchases | total_net_revenue | avg_daily_revenue |
|------|------|-----------------|-------------------|-------------------|
| 2022 | 6    | 50              | 15265.15          | 2544.19           |
| 2023 | 6    | 67              | 16573.31          | 2762.22           |
| 2024 | 6    | 68              | 26759.75          | 4459.96           |


---
