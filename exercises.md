# Retail Practice Exercises

**Dataset:** TechMart Electronics
**Format:** DuckDB

## Getting Started

Build the database from the CSV files in `data/`, or download a pre-built `retaildb.duckdb` from the [latest release](../../releases/latest):

```bash
duckdb retaildb.duckdb < build_db.sql
```

Before diving into the exercises, spend a few minutes exploring what's in it.

Some useful commands to get oriented:

```sql
-- What tables exist?
SHOW TABLES;

-- What columns does a table have?
DESCRIBE table_name;

-- What does the data look like?
SELECT * FROM table_name LIMIT 10;
```

## About These Exercises

These exercises are framed as real business questions -- deliberately vague, the way a stakeholder would actually ask them. Your job is to figure out what data answers the question, then write SQL to get it.

There is no single right answer for most of these. A query that answers the question in a reasonable way is a good query.

Each exercise includes collapsible **Hints**, **Solution**, and **Discussion** sections. Try to solve the exercise on your own before peeking.

---

## Beginner

### Exercise 1: "How many customers do we have?"

The CEO is prepping for a board meeting and needs a headcount.

<details>
<summary>Hints</summary>

- Where does customer data live?
- If I just count rows, will I get the right number?
- Could there be duplicate entries for the same customer?

</details>

<details>
<summary>Solution</summary>

`dim_customer` uses Type-2 SCD -- when a customer's `total_purchases` changes, a new row is created. A naive `COUNT(*)` returns 17,219 (all historical rows) instead of the real customer count.

**Using DISTINCT:**

```sql
SELECT COUNT(DISTINCT id) AS customer_count
FROM dim_customer;
```

**Only current customers:**

```sql
SELECT COUNT(*) AS current_customers
FROM dim_customer
WHERE valid_to IS NULL;
```

</details>

<details>
<summary>Discussion</summary>

Both approaches return 12,986. The first counts every customer who has ever existed. The second counts only the latest version of each. If the CEO wants "how many customers do we have right now," the second is more appropriate.

The key question to ask yourself: "I got 12,986, but the table has 17,219 rows. Why?" This leads naturally into SCD-2 concepts. The inflation is modest here because `total_purchases` only changes when a customer completes a purchase, and most customers don't purchase.

</details>

---

### Exercise 2: "What do we sell?"

A new hire on the analytics team needs to get familiar with the product catalog. Pull a quick summary.

<details>
<summary>Hints</summary>

- What does "summary" mean? A list of every product? Grouped by something?
- What information about products would be useful to see at a glance?
- How would you organize the output so it's easy to scan?

</details>

<details>
<summary>Solution</summary>

**Category summary:**

```sql
SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    MIN(price) AS cheapest,
    MAX(price) AS most_expensive
FROM dim_product
GROUP BY category
ORDER BY product_count DESC;
```

**Full catalog scan:**

```sql
SELECT
    id,
    name,
    category,
    price
FROM dim_product
ORDER BY category, price DESC;
```

</details>

<details>
<summary>Discussion</summary>

Running `SELECT * FROM dim_product LIMIT 10` explores the data but doesn't summarize it. Ask yourself: "If I had to explain our catalog in one table, what would it show?" The grouped version is more useful for a new hire getting oriented.

You may notice that product names look like person names (Elizabeth Clay, Nicholas Richmond) -- that's an artifact of the data generator. The 3 pinned products (TechMart Pro Laptop, TechMart Phone X, TechMart Wireless Earbuds) are the realistic ones.

</details>

---

### Exercise 3: "What did customers do on our busiest day?"

The ops team wants a recap of the single busiest day in the dataset -- how many actions happened and what types.

<details>
<summary>Hints</summary>

- How do you find the busiest day if you don't know which day it is?
- Can you do this in one query, or do you need to find the day first?
- What does "busiest" mean -- most total activity? Most purchases?

</details>

<details>
<summary>Solution</summary>

**Single-query approach:**

```sql
WITH daily_totals AS (
    SELECT
        timestamp::DATE AS day,
        COUNT(*) AS total_actions
    FROM fact_customer_action
    GROUP BY day
    ORDER BY total_actions DESC
    LIMIT 1
)
SELECT
    f.action_type,
    COUNT(*) AS action_count
FROM fact_customer_action f
WHERE f.timestamp::DATE = (SELECT day FROM daily_totals)
GROUP BY f.action_type
ORDER BY action_count DESC;
```

**Two-step approach:**

```sql
-- Step 1: Find the busiest day
SELECT timestamp::DATE AS day, COUNT(*) AS cnt
FROM fact_customer_action
GROUP BY day
ORDER BY cnt DESC
LIMIT 5;

-- Step 2: Use that date (once you know it)
SELECT action_type, COUNT(*) AS cnt
FROM fact_customer_action
WHERE timestamp::DATE = '2024-01-01'
GROUP BY action_type
ORDER BY cnt DESC;
```

</details>

<details>
<summary>Discussion</summary>

The busiest day is January 1, 2024 (~1,298 actions) -- the company's launch date when all initial customers arrived at once. This is a startup artifact, not a real business event. The next busiest days cluster in late December (Dec 21-22 at ~1,050-1,064) during the holiday season peak.

Reporting "our busiest day was January 1st" is technically correct but uncritical. Ask yourself: "Why would Jan 1 be busiest? Is it a real business spike or a data artifact?" Looking at the top 5 days and noticing December dominating the list (apart from Jan 1) shows more analytical thinking. The real finding: the late-December holiday surge drives peak activity.

If you notice Black Friday is missing from the top days, that's a great observation -- it connects to the infrastructure exercise later.

</details>

---

### Exercise 4: "Are weekends busier than weekdays?"

The warehouse manager wants to know if they should schedule more pickers on weekends.

<details>
<summary>Hints</summary>

- How do you get the day of the week from a timestamp?
- If there are more weekdays than weekend days in a year, does a simple SUM give a fair comparison?
- What's a fairer way to compare?

</details>

<details>
<summary>Solution</summary>

```sql
SELECT
    CASE
        WHEN EXTRACT(DOW FROM timestamp) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_actions,
    COUNT(*) / COUNT(DISTINCT timestamp::DATE) AS avg_daily_actions
FROM fact_customer_action
GROUP BY day_type;
```

**The common mistake:** Writing `COUNT(*)` without averaging gives a misleading result because weekdays outnumber weekends. There are 262 weekdays and 104 weekend days in 2024. A total comparison isn't fair -- you need the average per day.

</details>

<details>
<summary>Discussion</summary>

If you reported just totals: "There are 262 weekdays and 104 weekend days in 2024. Is a total comparison fair?" The data has a weekend surge -- both new arrivals and returning shoppers are more active on Sat/Sun. You should see a clear difference in average daily activity (roughly 35-40% higher on weekends). The behavioral explanation: people have more free time to browse on weekends.

</details>

---

## Intermediate

### Exercise 5: "Which product category makes us the most money?"

Quarterly business review. The product team wants to know where revenue concentrates.

<details>
<summary>Hints</summary>

- Is there a "revenue" column? If not, how do you calculate it?
- Where does product category live? Where do purchases live? How do you connect them?
- Does every row in the action table represent a sale?

</details>

<details>
<summary>Solution</summary>

There is no revenue column. Revenue = price of purchased products, which requires joining the action table to the product dimension and filtering to purchases only. Forgetting `WHERE action_type = 'purchase'` would count every product view and cart add as revenue.

```sql
SELECT
    p.category,
    COUNT(*) AS purchases,
    SUM(p.price) AS total_revenue,
    ROUND(AVG(p.price), 2) AS avg_price
FROM fact_customer_action f
JOIN dim_product p ON f.product_id = p.id
WHERE f.action_type = 'purchase'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

</details>

<details>
<summary>Discussion</summary>

Good follow-up questions to consider:
- "Is the highest-revenue category also the most profitable? How would you check?" (Use the `margin` column: `SUM(p.price * p.margin)`.)
- "Does the category with the most purchases always have the most revenue?" (Not necessarily -- accessories may sell in volume but at low prices.)

</details>

---

### Exercise 6: "Something weird happened around Black Friday. What do you see?"

Your manager pulls up a dashboard showing unusual activity around Thanksgiving week. "The pattern doesn't look like what I expected. Can you figure out what happened?"

<details>
<summary>Hints</summary>

- How do you look at traffic day by day?
- What would you *expect* to see around Black Friday? Does the data match?
- What could explain something unexpected?

</details>

<details>
<summary>Solution</summary>

**Daily activity around the holiday:**

```sql
SELECT
    timestamp::DATE AS day,
    COUNT(*) AS total_activity
FROM fact_customer_action
WHERE timestamp >= '2024-11-15' AND timestamp < '2024-12-15'
GROUP BY day
ORDER BY day;
```

**Quantify the pattern:**

```sql
WITH daily AS (
    SELECT timestamp::DATE AS day, COUNT(*) AS cnt
    FROM fact_customer_action
    GROUP BY day
),
baseline AS (
    SELECT AVG(cnt) AS avg_daily FROM daily
    WHERE day BETWEEN '2024-11-15' AND '2024-11-28'
)
SELECT
    d.day,
    d.cnt AS activity,
    ROUND(d.cnt / b.avg_daily, 1) AS multiple_of_average
FROM daily d, baseline b
WHERE d.day BETWEEN '2024-11-25' AND '2024-12-10'
ORDER BY d.day;
```

</details>

<details>
<summary>Discussion</summary>

You might expect a Black Friday spike. Instead, Nov 29 is **completely flat** (~0.94x baseline) -- indistinguishable from the surrounding weekdays. Then a massive **surge** starts Nov 30 through early December (1.6-1.7x baseline). This is the opposite of what anyone assumes.

The actual pattern: Black Friday (Nov 29) had ~556 actions -- essentially the same as the surrounding days (525-602). Then activity jumps sharply: Nov 30 (990), Dec 1 (998), Dec 2 Cyber Monday (998).

The question "why was Black Friday flat when we expected it to be huge?" is the real analytical challenge -- and it connects to the infrastructure exercise later. For now, the key takeaway is that an analyst's job is to describe what actually happened, not what they expected.

</details>

---

### Exercise 7: "Are we losing customers at checkout?"

The VP of Sales heard that cart abandonment is a problem. She wants to know if it's true and how bad it is.

<details>
<summary>Hints</summary>

- What actions tell you someone started checkout? What tells you they finished?
- Is the right metric a raw count or a rate?
- How do you identify customers who added to cart but never purchased?

</details>

<details>
<summary>Solution</summary>

**Customer-level abandonment:**

```sql
WITH cart_customers AS (
    SELECT DISTINCT customer_id
    FROM fact_customer_action
    WHERE action_type = 'add_to_cart'
),
purchase_customers AS (
    SELECT DISTINCT customer_id
    FROM fact_customer_action
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

**Per-session abandonment (more precise):**

```sql
WITH session_actions AS (
    SELECT
        session_id,
        customer_id,
        MAX(CASE WHEN action_type = 'add_to_cart' THEN 1 ELSE 0 END) AS had_cart_add,
        MAX(CASE WHEN action_type = 'purchase' THEN 1 ELSE 0 END) AS had_purchase
    FROM fact_customer_action
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

</details>

<details>
<summary>Discussion</summary>

The first approach answers "of all customers who ever added to cart, how many ever purchased?" It shows ~27% converted -- meaning ~73% of cart-adding customers never completed a purchase.

The second approach is more precise -- it looks at individual shopping sessions. Per-session, only ~9% of sessions with a cart add also have a purchase. The gap is dramatic: many customers add to cart in one session but only purchase in a later session (or never).

Discovering `session_id` and using it for session-level grouping is a sign of strong analytical thinking. The per-session view is especially important here because each shopping session completes quickly -- a customer's entire browse-to-purchase path happens in a single visit.

</details>

---

### Exercise 8: "I keep hearing we had a rough summer. Is that true?"

The head of growth saw a blog post about seasonal e-commerce trends and wants to know if TechMart follows the pattern.

<details>
<summary>Hints</summary>

- What months are "summer"?
- "Rough" compared to what -- spring? The full-year average? The same months' purchases?
- Could overall business growth mask a seasonal dip?

</details>

<details>
<summary>Solution</summary>

```sql
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', timestamp)::DATE AS month,
        COUNT(*) AS total_activity,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM fact_customer_action
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

</details>

<details>
<summary>Discussion</summary>

The picture is more nuanced than "summer bad." June is clearly below the annual average (~-15%), and July's growth decelerates sharply (only +8% MoM vs. +13% in June and +18% in August). But August recovers sharply -- rising above average due to back-to-school demand.

"Rough compared to what?" is the key question. Compared to the annual average, June is below (~-15%) and July barely reaches parity (~-8%), but August jumps above average (+9%) -- the back-to-school surge overpowers the tail end of the summer slowdown. Saying "summer was bad" based on June/July alone is partially right. Noticing that August breaks the pattern shows stronger analytical thinking.

The deeper lesson: the growing customer base creates an upward trend that masks seasonal effects. A thorough answer will try to detrend the data or compare month-over-month growth rates to isolate the summer slowdown from the growth curve.

</details>

---

## Advanced

### Exercise 9: "Do our premium customers actually spend more?"

Marketing segments customers as budget/mainstream/premium. The CFO asks: "Is that segmentation meaningful, or just marketing fluff?"

<details>
<summary>Hints</summary>

- "Spend more" could mean more purchases, higher-value items, more frequent visits, or better conversion rates
- How do you connect customer segments to their behavior?
- Is one metric enough, or do you need several to give a real answer?

</details>

<details>
<summary>Solution</summary>

**Purchases per customer by segment:**

```sql
SELECT
    c.segment,
    COUNT(DISTINCT c.id) AS customers,
    COUNT(CASE WHEN f.action_type = 'purchase' THEN 1 END) AS total_purchases,
    ROUND(
        COUNT(CASE WHEN f.action_type = 'purchase' THEN 1 END)::DECIMAL
        / NULLIF(COUNT(DISTINCT c.id), 0),
        2
    ) AS purchases_per_customer
FROM dim_customer c
JOIN fact_customer_action f ON c.id = f.customer_id
WHERE c.valid_to IS NULL
GROUP BY c.segment
ORDER BY purchases_per_customer DESC;
```

**With revenue per customer:**

```sql
SELECT
    c.segment,
    COUNT(DISTINCT c.id) AS customers,
    COUNT(CASE WHEN f.action_type = 'purchase' THEN 1 END) AS purchases,
    ROUND(
        SUM(CASE WHEN f.action_type = 'purchase' THEN p.price ELSE 0 END)::DECIMAL
        / NULLIF(COUNT(DISTINCT c.id), 0),
        2
    ) AS revenue_per_customer
FROM dim_customer c
JOIN fact_customer_action f ON c.id = f.customer_id
LEFT JOIN dim_product p ON f.product_id = p.id
WHERE c.valid_to IS NULL
GROUP BY c.segment
ORDER BY revenue_per_customer DESC;
```

</details>

<details>
<summary>Discussion</summary>

Premium customers convert from cart to purchase at 37% vs. 18% for budget -- and the difference compounds across the entire journey. The data shows premium at ~0.75 purchases per customer vs. budget at ~0.18 (about 4x). But "spend more" depends on definition -- if you measure average item price, the difference is smaller because product selection is popularity-weighted, not segment-weighted.

A basic answer checks one metric. A thorough answer checks several and synthesizes: "Premium buys more often (X vs Y purchases per customer), but average item value is similar because product selection isn't segment-driven. The real difference is conversion rate, not basket size."

</details>

---

### Exercise 10: "When should we staff up customer support?"

Operations needs to schedule the support team for peak hours. They want a recommendation backed by data.

<details>
<summary>Hints</summary>

- How do you get the hour from a timestamp?
- Does it matter what day of the week it is, or just the hour?
- What would a useful output look like -- a number? A table? A cross-tab of day and hour?

</details>

<details>
<summary>Solution</summary>

**Hourly breakdown:**

```sql
SELECT
    EXTRACT(HOUR FROM timestamp)::INT AS hour,
    COUNT(*) AS total_actions,
    ROUND(COUNT(*) / COUNT(DISTINCT timestamp::DATE)::DECIMAL, 1) AS avg_actions_per_day
FROM fact_customer_action
GROUP BY hour
ORDER BY hour;
```

**Hour x Day-of-week cross-tab:**

```sql
WITH hourly_daily AS (
    SELECT
        timestamp::DATE AS day,
        EXTRACT(HOUR FROM timestamp)::INT AS hour,
        CASE WHEN EXTRACT(DOW FROM timestamp) IN (0, 6) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
        COUNT(*) AS actions
    FROM fact_customer_action
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

</details>

<details>
<summary>Discussion</summary>

The data has clear hourly patterns: evening peak (17-21), morning shopping (9-12), and low early-morning activity (6-9). The recommendation matters as much as the query -- a useful answer says something like "Staff heaviest 5-9pm, moderate 9am-noon, skeleton crew before 9am."

</details>

---

### Exercise 11: "Who are our most valuable customers beyond the VIP list?"

The sales team sees about 77 customers tagged as VIP in the system. They think the real list of high-value customers is bigger. Can you find who else deserves attention?

<details>
<summary>Hints</summary>

- What makes someone "high value" -- purchases? Spending? Frequency? All of the above?
- How do you combine customer data with their actual purchase history?
- How do you rank customers when there are multiple ways to measure value?
- How many should be on the list?

</details>

<details>
<summary>Solution</summary>

**Multi-criteria scoring:**

```sql
WITH customer_stats AS (
    SELECT
        c.id,
        c.name,
        c.segment,
        c.tier,
        c.income,
        COUNT(CASE WHEN f.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(*) AS total_actions,
        COUNT(DISTINCT f.session_id) AS visits
    FROM dim_customer c
    JOIN fact_customer_action f ON c.id = f.customer_id
    WHERE c.valid_to IS NULL
    GROUP BY c.id, c.name, c.segment, c.tier, c.income
)
SELECT
    id,
    name,
    segment,
    tier,
    purchases,
    visits,
    income,
    NTILE(10) OVER (ORDER BY purchases DESC) AS purchase_decile
FROM customer_stats
WHERE tier != 'vip'
ORDER BY purchases DESC, visits DESC
LIMIT 25;
```

</details>

<details>
<summary>Discussion</summary>

The exercise deliberately frames it as "beyond the VIP list." A good first step is to run `SELECT * FROM dim_customer WHERE tier = 'vip'` to see the existing ~77 VIPs -- understanding what exists before building on it. The real task is identifying high-value non-VIP customers.

The pinned customers (Alexandra Chen, Marcus Johnson, Sofia Rodriguez) are already VIPs, so they should be filtered out. Building a scoring system that combines purchases, visits, and income shows analytical maturity.

</details>

---

### Exercise 12: "Are customers from paid search worth the money?"

The marketing budget is under review. Someone asks if paid search customers perform as well as organic ones.

<details>
<summary>Hints</summary>

- Where is acquisition channel stored?
- What does "worth the money" mean? Convert better? Buy more often? Higher value purchases?
- How do you compare two groups fairly?

</details>

<details>
<summary>Solution</summary>

```sql
WITH channel_metrics AS (
    SELECT
        c.acquisition_source AS channel,
        COUNT(DISTINCT c.id) AS customers,
        COUNT(CASE WHEN f.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT CASE WHEN f.action_type = 'purchase' THEN c.id END) AS buyers,
        COUNT(DISTINCT f.session_id) AS total_sessions
    FROM dim_customer c
    JOIN fact_customer_action f ON c.id = f.customer_id
    WHERE c.valid_to IS NULL
    GROUP BY c.acquisition_source
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

</details>

<details>
<summary>Discussion</summary>

Customers are distributed across channels (roughly 40% organic, 30% paid_search, 20% social, 10% referral) with no behavioral difference by channel. A thorough answer recognizes: "There's no meaningful difference -- acquisition source doesn't affect behavior." That's a valid and important finding. In real life, this means the marketing team shouldn't assume paid search is worse (or better) without additional data like cost per acquisition.

</details>

---

## Expert

### Exercise 13: "Customers browse a lot but don't seem to buy. What's going on?"

The product manager shows you a chart: tons of product views, but low purchase numbers. She wants to understand the gap.

<details>
<summary>Hints</summary>

- What does the path from browsing to buying look like in this data?
- Is the problem the same for all customer types, or do some segments convert better?
- Can you build a "funnel" from the different action types?
- Where is the biggest drop-off?

</details>

<details>
<summary>Solution</summary>

**Funnel by segment:**

```sql
WITH funnel AS (
    SELECT
        c.segment,
        COUNT(DISTINCT c.id) AS total_customers,
        COUNT(DISTINCT CASE WHEN f.action_type = 'product_view' THEN c.id END) AS viewers,
        COUNT(DISTINCT CASE WHEN f.action_type = 'add_to_cart' THEN c.id END) AS carted,
        COUNT(DISTINCT CASE WHEN f.action_type = 'purchase' THEN c.id END) AS purchasers
    FROM dim_customer c
    JOIN fact_customer_action f ON c.id = f.customer_id
    WHERE c.valid_to IS NULL
    GROUP BY c.segment
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

</details>

<details>
<summary>Discussion</summary>

About 70% of customers view products, and roughly half of viewers add to cart (30% per-visit probability). The biggest drop-off is from cart to purchase: only ~18% of budget cart-adders purchase vs. ~37% of premium. So the answer is layered: "Most customers browse and many add to cart, but the conversion from cart to purchase is where segments diverge dramatically. Premium converts at about 2x the budget rate."

Computing an overall view-to-purchase ratio gives you a number. Building a funnel by action type AND breaking it down by segment gives you an actionable insight. Ask yourself: "If you could only fix one part of the funnel, which step and which segment would you target?"

</details>

---

### Exercise 14: "Did the spring sale actually work?"

Marketing ran a flash sale March 15-17. Finance wants to know if it moved the needle, or if they should cut the budget next year.

<details>
<summary>Hints</summary>

- "Worked" compared to what? You need a baseline.
- What's the right baseline -- the week before? The whole month? Same weekdays?
- "Moved the needle" on what -- traffic? Cart adds? Purchases?
- Could the sale have just pulled purchases forward from the following week (cannibalization)?

</details>

<details>
<summary>Solution</summary>

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
    FROM fact_customer_action
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

</details>

<details>
<summary>Discussion</summary>

The spring flash sale doubled add_to_cart probability (0.30 to 0.60), but the averaged result over the 3-day period looks underwhelming -- only a modest lift in daily cart adds. The explanation requires looking day by day:

- **March 15 (sale day 1):** An infrastructure outage (INFRA_0001 went degraded) fires on the same day. The outage blocks re-entry for all returning customers, so only new arrivals generate sessions. The doubled cart-add rate applies to far fewer sessions. Net result: suppressed activity despite the sale.
- **March 16-17 (sale days 2-3):** Infrastructure recovers, re-entry resumes, and the doubled cart-add rate operates on normal session volume. These days should show a cleaner lift vs. the prior week.

Averaging all three days gives a misleading "the sale barely worked." Looking day by day reveals the truth: the sale worked on the days it wasn't confounded by the outage.

This teaches two critical lessons: (1) always look at the data before averaging -- a single suppressed day can drag down a period average, and (2) real-world experiments rarely have clean control periods. Confounding events are the norm, not the exception.

Consider also: "The sale started the same day as a system outage. How does that complicate your analysis?" and "Check the week after. Did cart adds drop below normal? If so, the sale may have cannibalized future demand rather than creating new demand." Noticing the outage confound (discoverable via `dim_infrastructure`) without being told to look shows exceptional analytical instinct.

</details>

---

### Exercise 15: "Which customers should we worry about?"

The retention team has budget for outreach to 50 customers. Who should they contact?

<details>
<summary>Hints</summary>

- "Worry about" means at-risk, but at risk of what? Leaving? Not buying again?
- How do you define "at risk" from behavior data?
- Could you look at customers who used to be active but have gone quiet?
- How do you rank risk and pick the top 50?

</details>

<details>
<summary>Solution</summary>

```sql
WITH customer_activity AS (
    SELECT
        c.id,
        c.name,
        c.segment,
        c.income,
        COUNT(*) AS total_actions,
        MAX(f.timestamp) AS last_activity,
        COUNT(CASE WHEN f.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT f.session_id) AS sessions
    FROM dim_customer c
    JOIN fact_customer_action f ON c.id = f.customer_id
    WHERE c.valid_to IS NULL AND c.active = true
    GROUP BY c.id, c.name, c.segment, c.income
),
risk_scored AS (
    SELECT
        *,
        DATE_DIFF('day', last_activity::DATE, '2024-12-31') AS days_inactive,
        CASE WHEN sessions > 1 AND purchases = 0 THEN 1 ELSE 0 END AS engaged_non_buyer
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
ORDER BY engaged_non_buyer DESC, days_inactive DESC
LIMIT 50;
```

</details>

<details>
<summary>Discussion</summary>

The definition of "at risk" is entirely up to you. Some valid approaches:
- **Recency-based:** Customers who haven't been seen in 30+ days
- **Engagement-based:** Customers who browse but never buy (many sessions, zero purchases)
- **Value-based:** High-income customers who went quiet (highest opportunity cost)
- **Combined:** Score using multiple factors

All are defensible. The exercise forces you to make a judgment call and explain it.

</details>

---

### Exercise 16: "Build me something that shows how the business is doing."

The CEO is tired of asking one-off questions. She wants a query she can run monthly that tells her whether things are on track.

<details>
<summary>Hints</summary>

- What metrics actually tell you if a business is healthy?
- How do you show trend direction (getting better / getting worse)?
- Can you show month-over-month change?
- What would make this useful for someone who doesn't write SQL?
- A basic answer shows one metric. A strong answer shows a dashboard.

</details>

<details>
<summary>Solution</summary>

**Monthly executive dashboard:**

```sql
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', f.timestamp)::DATE AS month,
        COUNT(*) AS total_activity,
        COUNT(DISTINCT f.customer_id) AS active_customers,
        COUNT(CASE WHEN f.action_type = 'visit' THEN 1 END) AS new_visits,
        COUNT(CASE WHEN f.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT CASE WHEN f.action_type = 'purchase' THEN f.customer_id END) AS buyers
    FROM fact_customer_action f
    WHERE f.timestamp < '2025-01-01'
    GROUP BY month
),
with_trends AS (
    SELECT
        month,
        active_customers,
        new_visits,
        purchases,
        buyers,
        ROUND(100.0 * buyers / NULLIF(active_customers, 0), 1) AS conversion_rate,
        LAG(purchases) OVER (ORDER BY month) AS prev_month_purchases,
        ROUND(100.0 * (purchases - LAG(purchases) OVER (ORDER BY month))
            / NULLIF(LAG(purchases) OVER (ORDER BY month), 0), 1) AS purchase_growth_pct,
        ROUND(100.0 * (active_customers - LAG(active_customers) OVER (ORDER BY month))
            / NULLIF(LAG(active_customers) OVER (ORDER BY month), 0), 1) AS customer_growth_pct
    FROM monthly
)
SELECT
    month,
    active_customers,
    new_visits,
    purchases,
    conversion_rate AS conversion_pct,
    purchase_growth_pct AS mom_purchase_growth,
    customer_growth_pct AS mom_customer_growth
FROM with_trends
ORDER BY month;
```

**What makes a strong answer:**

| Basic | Moderate | Strong |
|-------|----------|--------|
| One metric, one query | Multiple metrics, grouped by month | Trend + comparison + multiple dimensions |
| `SELECT COUNT(*) FROM fact_customer_action` | Monthly purchase counts | MoM growth, conversion rate, customer growth |
| No context for interpretation | Absolute numbers | Rates and changes that show direction |

</details>

<details>
<summary>Discussion</summary>

This is the capstone because it combines everything: CTEs, window functions (LAG), aggregation, date truncation, CASE, and analytical thinking. There's no single right answer. The quality shows in whether the output helps someone make decisions without further questions.

A CEO-friendly output has: few columns, clear labels, trend direction (up/down), and rates rather than raw counts. Producing a wall of numbers shows SQL skills but not yet analytical judgment.

</details>

---

### Exercise 17: "Black Friday was supposed to be our biggest day. What went wrong?"

The head of e-commerce is upset. "We planned a massive Black Friday campaign -- 4x the normal ad spend. But when I look at the numbers, November 29th was just... average. No spike at all. What happened?"

<details>
<summary>Hints</summary>

- Start by looking at daily traffic around Black Friday. Is the claim true?
- If Black Friday really was low, what happened on the days right after?
- You have more data available than just customer actions. Could something operational explain this?
- Can you quantify the impact -- how much traffic was lost, and did it come back?

</details>

<details>
<summary>Solution</summary>

**Step 1: Confirm the claim -- was Black Friday really bad?**

```sql
WITH daily AS (
    SELECT timestamp::DATE AS day, COUNT(*) AS activity
    FROM fact_customer_action
    GROUP BY day
),
baseline AS (
    SELECT AVG(activity) AS avg_daily
    FROM daily
    WHERE day BETWEEN '2024-11-15' AND '2024-11-28'
)
SELECT
    d.day,
    d.activity,
    ROUND(d.activity / b.avg_daily, 2) AS vs_baseline
FROM daily d, baseline b
WHERE d.day BETWEEN '2024-11-25' AND '2024-12-07'
ORDER BY d.day;
```

Nov 29 shows ~0.94x baseline -- essentially a normal day despite being Black Friday. Then Nov 30 onward surges to 1.6-1.7x. The claim is true -- Black Friday was flat when it should have been huge.

**Step 2: Discover the infrastructure table**

```sql
SELECT * FROM dim_infrastructure ORDER BY valid_from;
```

The `dim_infrastructure` table has SCD-2 rows showing three outage events across the year. If you haven't explored this table yet, ask yourself: "Are there any other tables in the database I haven't looked at?"

**Step 3: Connect the outage to the dip**

```sql
SELECT
    id,
    status,
    error_rate,
    valid_from::DATE AS started,
    valid_to::DATE AS ended
FROM dim_infrastructure
WHERE id = 'INFRA_0001'
ORDER BY valid_from;
```

INFRA_0001 went `degraded` on exactly 2024-11-29 and recovered on 2024-11-30. The timing matches perfectly -- the outage ate the expected Black Friday boost.

**Step 4 (thorough answer): Quantify all outage impacts**

```sql
WITH outages AS (
    SELECT
        valid_from::DATE AS outage_date,
        valid_to::DATE AS recovery_date
    FROM dim_infrastructure
    WHERE id = 'INFRA_0001' AND status = 'degraded'
),
daily AS (
    SELECT timestamp::DATE AS day, COUNT(*) AS activity
    FROM fact_customer_action
    GROUP BY day
)
SELECT
    o.outage_date,
    d_during.activity AS outage_day_activity,
    d_before.activity AS day_before_activity,
    d_after.activity AS day_after_activity,
    ROUND(100.0 * d_during.activity / d_before.activity, 1) AS pct_of_prior_day
FROM outages o
JOIN daily d_during ON d_during.day = o.outage_date
JOIN daily d_before ON d_before.day = o.outage_date - INTERVAL '1 day'
JOIN daily d_after ON d_after.day = o.recovery_date
ORDER BY o.outage_date;
```

</details>

<details>
<summary>Discussion</summary>

This exercise teaches root cause analysis. The business question is "what went wrong?" and the answer isn't in the customer data -- it's in an operational table you might not have noticed. This mirrors real analytics work: the explanation for a metric moving isn't always in the same table as the metric.

Multiple levels of depth:

| Level | What you find |
|-------|--------------|
| Basic | "Yes, Nov 29 was flat" (confirms the claim, stops there) |
| Moderate | Finds the infrastructure table, connects the outage to the date |
| Thorough | Quantifies the impact, checks the recovery pattern, finds all three outages |
| Exceptional | Notes that the Nov 30-Dec 2 surge (1.6-1.7x) far exceeded the Nov 28 baseline -- suggesting pent-up demand from the outage, not just normal holiday growth |

Follow-up questions to consider:
- "If you were the head of e-commerce, what would you recommend for next Black Friday?"
- "The system shows three outages in 2024. Is there a pattern?"
- "How would you estimate how much revenue the Black Friday outage cost?"

</details>
