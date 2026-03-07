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
DESCRIBE retaildb.main.table_name;

-- What does the data look like?
SELECT * FROM retaildb.main.dim_customer LIMIT 10;
```

## About These Exercises

These exercises are framed as real business questions -- deliberately vague, the way a stakeholder would actually ask them. Your job is to figure out what data answers the question, then write SQL to get it.

There is no single right answer for most of these. A query that answers the question in a reasonable way is a good query.

Each exercise includes collapsible **Hints**, **Solution**, and **Discussion** sections. Try to solve the exercise on your own before peeking. Solutions provided are one way to answer the question. You might find better solutions. 

Pro Tip: You may want to dump some of your query results into Excel or Sheets then create a chart. Patterns are much easier to see visually. 

Another Pro Tip: Feel free to let an LLM help you when you get stuck. There's nothing wrong with getting help wherever it exists. Just start with a prompt like "I am learning SQL and want a mentor who will teach me how to understand the needed query instead of simply providing an answer." 

DuckDB: You may have never seen casting like timestamp::date. Some DBMS support this and some don't. Don't worry, it's just short for cast(timestamp as date). Probably my favorite convenience that has become more popular in recent years. 

---

## Warming Up 

### Exercise 1: "How many customers do we have?"

The CEO is prepping for a board meeting and needs a headcount.

<details>
<summary>Hints</summary>

- Where does customer data live?
- Could there be duplicate entries for the same customer?
- What is a customer?  

</details>

<details>
<summary>Solution</summary>

`dim_customer` uses Type-2 SCD -- when a customer's `total_purchases` changes, a new row is created. A naive `COUNT(*)` returns 13,294 (all historical rows) instead of the real customer count.

**Using DISTINCT:**

```sql
SELECT 
    COUNT(DISTINCT id) AS customer_count
FROM retaildb.main.dim_customer;
```

**Only current customers:**

```sql
SELECT COUNT(*) AS current_customers
FROM retaildb.main.dim_customer
WHERE valid_to IS NULL;
```

Customers as people who purchased something. 

```sql
SELECT 
    COUNT(DISTINCT id) AS customer_count
FROM retaildb.main.dim_customer
WHERE total_purchases > 0;
```

Same data, but from the fact table. 

```sql
SELECT
    count(distinct customer_id) as num_customers
FROM retaildb.main.fact_customer_action
WHERE action_type = 'purchase'
```

</details>

<details>
<summary>Discussion</summary>

Both approaches return 9,074. The first deduplicates across all historical rows (SCD-2 creates multiple rows per customer). The second counts only the latest version of each. If the CEO wants "how many customers do we have right now," the second is more appropriate.

The key question to ask yourself: "I got 9,074, but the table has 13,294 rows. Why?" This leads naturally into SCD-2 concepts you can research. The inflation is modest here because `total_purchases` only changes when a customer completes a purchase, and most customers don't purchase.

But wait, there's more! The real question here is what is a customer? Our customers table includes anyone that ever signed into our site. Some may say that is the definition of a prospect or a lead. Another definition of customer could be all people who have purchased a product. We can get that by querying dim_customer or fact_customer_action and get 663. 

Side note: Stuff like this happens all the time. One team measures X one way, but other teams measure it differently. This is the time to be pedantic and agree on a definition. 

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
FROM retaildb.main.dim_product
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
FROM retaildb.main.dim_product
ORDER BY category, price DESC;
```

</details>

<details>
<summary>Discussion</summary>

Running `SELECT * FROM retaildb.main.dim_product LIMIT 10` explores the data but doesn't summarize it. Ask yourself: "If I had to explain our catalog in one table, what would it show?" The grouped version is more useful for a new hire getting oriented.

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

**Two-step approach:**

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

</details>

<details>
<summary>Discussion</summary>

The busiest day is a real business event -- the Sunday before Christmas, a peak holiday-shopping day in late December. Look at the top 5 days and you'll see several fall in late November and December, though high-traffic weekends in other months also appear. Notably, Sep 22 (675 actions) nearly equals the #1 day and isn't holiday-related -- it's just a high-traffic Sunday.

Ask yourself: "Why was this day the busiest? Does the explanation make business sense?" If you see multiple top days in the same window, that's the holiday surge at work. The dataset spans nearly three years, so you can also check whether the same pattern repeats each year. Maybe creating a chart would help. 

If you notice that Black Friday (Nov 29, 2024) is missing from the top days when it is usually the busiest day of the year, that's a great observation -- it connects to a later exercise.  

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
    COUNT(*) * 1.0 / COUNT(DISTINCT timestamp::DATE) AS avg_daily_actions
FROM retaildb.main.fact_customer_action
GROUP BY day_type;
```

**The common mistake:** Writing `COUNT(*)` without averaging gives a misleading result because weekdays outnumber weekends -- there are roughly 2.5x as many weekdays as weekend days in any given period. A total comparison isn't fair -- you need the average per day.

</details>

<details>
<summary>Discussion</summary>

If you reported just totals, consider: there are roughly 2.5x as many weekdays as weekend days. Is a total comparison fair? The data has a weekend surge -- both new and returning shoppers are more active on Sat/Sun. You should see a clear difference in average daily activity (about 47% higher on weekends). The behavioral explanation: people have more free time to browse on weekends.

</details>

---

## Digging In 

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

There is no revenue column. Revenue = price * quantity of purchased products, which requires joining the action table to the product dimension and filtering to purchases only. Forgetting `WHERE action_type = 'purchase'` would count every product view and cart add as revenue.

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

</details>

<details>
<summary>Discussion</summary>

Good follow-up questions to consider:
- "Is the highest-revenue category also the most profitable? How would you check?" (Use the `margin` column: `SUM(product.price * actions.quantity * product.margin)`.)
- Note: the query above calculates **gross (list-price) revenue**. The `discount_pct` column is available if you want to compute net revenue: `SUM(product.price * actions.quantity * (1 - actions.discount_pct))`. Exercise 19 uses this net formula -- the difference is about 7.5% on average.
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
FROM retaildb.main.fact_customer_action
WHERE timestamp >= '2024-11-15' AND timestamp < '2024-12-15'
GROUP BY day
ORDER BY day;
```

**Quantify the pattern:**

```sql
WITH daily AS (
    SELECT 
        timestamp::DATE AS day, 
        COUNT(*) AS cnt
    FROM retaildb.main.fact_customer_action
    GROUP BY day
),
baseline AS (
    SELECT 
        AVG(cnt) AS avg_daily 
    FROM daily
    WHERE day BETWEEN '2024-11-15' AND '2024-11-28'
)
SELECT
    daily.day,
    daily.cnt AS activity,
    ROUND(daily.cnt / baseline.avg_daily, 1) AS multiple_of_average
FROM daily 
CROSS JOIN baseline
WHERE daily.day BETWEEN '2024-11-25' AND '2024-12-10'
ORDER BY daily.day;
```

</details>

<details>
<summary>Discussion</summary>

You might expect a massive Black Friday spike. Instead, Nov 29, 2024 drops to 0.5x baseline -- well below an average day. Meanwhile, Cyber Monday (Dec 2) surges to 1.6x. The surrounding days (Nov 30 through Dec 4, 1.4-1.6x) all dramatically outperform Black Friday. Something suppressed the expected spike.

The dataset covers nearly three years. Compare Black Friday across years (Nov 25 in 2022, Nov 24 in 2023, Nov 29 in 2024): in 2022 and 2023, Black Friday is among the highest-traffic days in its week. In 2024, it doesn't -- Nov 30 and Dec 1-2 all beat it. The question "why didn't 2024 Black Friday spike like previous years?" is the real analytical challenge -- Can you figure it out? The data to solve this is available, but don't worry. There's a more specific exercise later.  


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

**Per-session abandonment (more precise):**

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

</details>

<details>
<summary>Discussion</summary>

The first approach answers "of all customers who ever added to cart, how many ever purchased?" It shows only 8.9% converted -- meaning 91.1% of cart-adding customers never completed a purchase. The VP's concern is very much confirmed.

The second approach looks at individual shopping sessions. Per-session, 9.0% of sessions with a cart add also have a purchase -- similar to the customer-level rate. This tells you the cart-to-purchase conversion probability is roughly consistent whether measured per-customer or per-session.

If you discovered `session_id` and used it for session-level grouping, great job! The per-session view is especially important here because within any given session, a customer's browse-to-purchase path completes in that single visit (view → cart → purchase), though individual customers typically purchase across multiple sessions over time.

Damn! That's really high abandonment. The natural question to ask is why? Unfortunately, you don't have any data that explains it. My guess, annoying popups or a flawed checkout flow. Or, more likely, the author misconfigured his data generator and don't want to fix it and QA every exercise again. *my bad*.

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

**Month-over-month growth rates:**

The discussion below analyzes MoM growth, so here's a query to compute it:

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

</details>

<details>
<summary>Discussion</summary>

The picture is more nuanced than "summer bad." Look at month-over-month growth rates: June tends to show decelerating growth (low single digits in 2023 and 2024, down from stronger spring months), and July is inconsistent -- it held steady in 2023 (3.8%) but dipped to −0.3% in 2024. August and September tend to recover. The summer slowdown is real but short-lived.

As the great philosopher [Marcel the Shell with Shoes On](https://youtu.be/VF9-sEbqDvU?si=9uLV8gGym08nyJuw&t=162) once said, "Compared to what?". This is the key question. Saying "summer was bad" based on June/July alone is partially right. Noticing that August breaks the pattern shows stronger analytical thinking. With nearly three years of data, you can check whether this pattern repeats each summer -- and in 2023-2024, it does (2022 is harder to read because the business was still in early growth).

The deeper lesson: the growing customer base creates an upward trend that masks seasonal effects. Comparing to an overall average across 34 months is misleading because early months are tiny and late months are large. A thorough answer will compare month-over-month growth rates or look at the same months across years to isolate the summer slowdown from the growth curve.

</details>

---

## Putting All Your Knowledge to Good Use 

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
    customer.segment,
    COUNT(DISTINCT customer.id) AS customers,
    COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS total_purchases,
    ROUND(
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END)::DECIMAL
        / NULLIF(COUNT(DISTINCT customer.id), 0),
        2
    ) AS purchases_per_customer
FROM retaildb.main.dim_customer customer
LEFT JOIN retaildb.main.fact_customer_action actions 
    ON customer.id = actions.customer_id
WHERE customer.valid_to IS NULL
GROUP BY customer.segment
ORDER BY purchases_per_customer DESC;
```

**With revenue per customer:**

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
LEFT JOIN retaildb.main.fact_customer_action actions 
    ON customer.id = actions.customer_id
LEFT JOIN retaildb.main.dim_product product 
    ON actions.product_id = product.id
WHERE customer.valid_to IS NULL
GROUP BY customer.segment
ORDER BY revenue_per_customer DESC;
```

</details>

<details>
<summary>Discussion</summary>

Premium customers buy significantly more often: 1.65 purchases per customer vs. budget at 0.44 (about 3.8x). Looking at the funnel (Exercise 13), premium converts from cart to purchase at 15.9% vs. 5.8% for budget -- and the difference compounds throughout the three-year period. But "spend more" depends on definition -- if you measure average item price, the difference is smaller.

A basic answer checks one metric. A thorough answer checks several and synthesizes: "Premium buys more often (1.65 vs 0.44 purchases per customer), but average item value is similar because product selection isn't segment-driven. The real difference is purchase frequency and conversion rate, not basket size." You could also look at the quantity of items purchased. Right now, we are equating a purchase of one item, but there is a quantity field as well. Does that change anything? 

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
FROM retaildb.main.fact_customer_action
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
    FROM retaildb.main.fact_customer_action
    GROUP BY 
        day, 
        hour, 
        day_type
)
SELECT
    hour,
    day_type,
    ROUND(AVG(actions), 1) AS avg_actions
FROM hourly_daily
GROUP BY 
    hour, 
    day_type
ORDER BY 
    hour, 
    day_type;
```

</details>

<details>
<summary>Discussion</summary>

The data has clear hourly patterns: evening peak (17-20), morning shopping (9-11), and low early-morning activity (6-8). The recommendation matters as much as the query -- a useful answer says something like "Staff heaviest 5-8pm, moderate 9-11am, skeleton crew before 9am." If you ran the weekend vs. weekday breakdown, you'll notice weekends are consistently higher across all hours -- another factor for staffing decisions.

</details>

---

### Exercise 11: "Who are our most valuable customers beyond the VIP list?"

The sales team sees about 40 customers tagged as VIP in the system. They think the real list of high-value customers is bigger. Can you find who else deserves attention?

<details>
<summary>Hints</summary>

- What makes someone "high value" -- purchases? Spending? Frequency? All of the above?
- How do you combine customer data with their actual purchase history?
- How do you rank customers when there are multiple ways to measure value?
- How many should be on the list?

</details>

<details>
<summary>Solution</summary>

**Sorting by multiple criteria:**

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
    INNER JOIN retaildb.main.fact_customer_action actions 
        ON customer.id = actions.customer_id
    WHERE customer.valid_to IS NULL
    GROUP BY 
        customer.id, 
        customer.name, 
        customer.segment, 
        customer.tier, 
        customer.income
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
ORDER BY 
    purchases DESC, 
    visits DESC
LIMIT 25;
```

</details>

<details>
<summary>Discussion</summary>

The exercise deliberately frames it as "beyond the VIP list." A good first step is to run `SELECT * FROM retaildb.main.dim_customer WHERE tier = 'vip' AND valid_to IS NULL` to see the existing 40 VIPs -- understanding what exists before building on it. The real task is identifying high-value non-VIP customers.

You'll notice that not all VIPs are equally active -- only about 30% ever purchased while the rest browsed but never purchased. Think of it as a VIP signup program with 30% conversion. Building a scoring system that combines purchases, visits, and income would be a great solution.  

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
        customer.acquisition_source AS channel,
        COUNT(DISTINCT customer.id) AS customers,
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'purchase' THEN customer.id END) AS buyers,
        COUNT(DISTINCT actions.session_id) AS total_sessions
    FROM retaildb.main.dim_customer customer
    LEFT JOIN retaildb.main.fact_customer_action actions 
        ON customer.id = actions.customer_id
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

</details>

<details>
<summary>Discussion</summary>

Customers are distributed across channels (40% organic, 30% paid_search, 20% social, 10% referral). The buyer percentage is similar across channels (6.8-7.7%), but purchases per customer shows a gradient: organic (0.86) outperforms paid_search (0.79), social (0.74), and referral (0.64). Whether this gradient is meaningful depends on context -- with thousands of customers per channel, even small differences could matter, but without cost-per-acquisition data you can't determine ROI. A thorough answer acknowledges the gradient while noting that acquisition source alone doesn't tell you which channel is most cost-effective.

</details>

---

## This Is Getting Harder 

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
        customer.segment,
        COUNT(DISTINCT customer.id) AS total_customers,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'product_view' THEN customer.id END) AS viewers,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'add_to_cart' THEN customer.id END) AS carted,
        COUNT(DISTINCT CASE WHEN actions.action_type = 'purchase' THEN customer.id END) AS purchasers
    FROM retaildb.main.dim_customer customer
    LEFT JOIN retaildb.main.fact_customer_action actions 
        ON customer.id = actions.customer_id
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

</details>

<details>
<summary>Discussion</summary>

About 80-82% of customers view products. The biggest drop-off is from cart to purchase: only 5.8% of budget cart-adders purchase vs. 15.9% of premium. So the answer is layered: "Most customers browse and most add to cart, but the conversion from cart to purchase is where segments diverge dramatically. Premium converts at about 2.7x the budget rate."

Computing an overall view-to-purchase ratio gives you a number. Building a funnel by action type AND breaking it down by segment gives you an actionable insight. Ask yourself: "If you could only fix one part of the funnel, which step and which segment would you target?"

You may notice that our query creates view_to_cart_pct > 100. That's because some customers add to cart without a `product_view` event, so there are more distinct "carters" than "viewers." This means the customer-level funnel doesn't capture the real view-to-cart drop-off. We don't have the data to figure out why, but it is worth noting and not unusual. Maybe products were added to cart from apps instead of the website. Unfortunately, this dataset doesn't tell us.  
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

After digging deeper you found something odd. 

```sql
select 
    timestamp::date as day,
    count(*) as num_actions
from retaildb.main.fact_customer_action
where timestamp between '2024-03-08' and '2024-03-24'
group by timestamp::date 
order by timestamp::date
```

</details>

<details>
<summary>Discussion</summary>

The 3-day sale period average looks underwhelming -- lower daily cart adds (~19% decrease) than the surrounding weeks. But the averaged result hides a massive confounder. Look day by day:

- **March 15 (sale day 1):** Only 30 total actions -- a catastrophic drop from the ~331/day baseline. An infrastructure outage (INFRA_0001 went degraded.) fires on the same day. The outage blocks existing customers (Can you find that in the data?), so only new customers generate sessions. This single day drags the 3-day average down well below baseline.
- **March 16-17 (sale days 2-3):** Infrastructure recovers and activity surges (450 and 401 actions). Any sale effect is hard to disentangle from the natural weekend recovery and pent-up demand.

The key lesson isn't whether the sale "worked" -- it's that **you can't evaluate a 3-day promotion when 1/3 of it was wiped out by a system outage**. Averaging all three days gives a misleading "the sale barely worked." Looking day by day reveals that the outage is the dominant signal, not the sale.

This teaches two critical lessons: (1) always look at the data before averaging -- a single suppressed day can drag down a period average, and (2) real-world experiments rarely have clean control periods. Confounding events are the norm, not the exception.

Consider also: "The sale started the same day as a system outage. How does that complicate your analysis?" and "Check the week after. Did cart adds drop below normal? If so, the sale may have cannibalized future demand rather than creating new demand." Noticing the outage confound (discoverable via `dim_infrastructure`) explains a lot about what happened.  

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
        customer.id,
        customer.name,
        customer.segment,
        customer.income,
        COUNT(*) AS total_actions,
        MAX(actions.timestamp) AS last_activity,
        COUNT(CASE WHEN actions.action_type = 'purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT actions.session_id) AS sessions
    FROM retaildb.main.dim_customer customer
    INNER JOIN retaildb.main.fact_customer_action actions 
        ON customer.id = actions.customer_id
    WHERE 
        customer.valid_to IS NULL 
        AND customer.active = true
    GROUP BY 
        customer.id, 
        customer.name, 
        customer.segment, 
        customer.income
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

</details>

<details>
<summary>Discussion</summary>

The definition of "at risk" is entirely up to you. Some valid approaches:
- **Recency-based:** Customers who haven't been seen in 30+ days
- **Engagement-based:** Customers who browse but never buy (high activity, zero purchases)
- **Value-based:** High-income customers who went quiet 
- **Combined:** Score using multiple factors

All are defensible. The exercise forces you to dig into the data and  make a judgment call that explains it. You may notice that all these "customers" never purchased anything. I wonder if focusing on customers who have purchased but not in a long time would be useful. This is a great time to think about cohorts. How do we group customers with similar behavior. 

</details>

---

## The Capstone

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

**What makes a strong answer:**

| Basic | Moderate | Strong |
|-------|----------|--------|
| One metric, one query | Multiple metrics, grouped by month | Trend + comparison + multiple dimensions |
| `SELECT COUNT(*) FROM fact_customer_action` | Monthly purchase counts | MoM growth, conversion rate, customer growth |
| No context for interpretation | Absolute numbers | Rates and changes that show direction |

</details>

<details>
<summary>Discussion</summary>

This is a capstone because it combines everything: CTEs, window functions (LAG), aggregation, date truncation, CASE, and analytical thinking. There's no single right answer. The quality shows in whether the output helps someone make decisions without further questions.

A CEO-friendly output has: few columns, clear labels, trend direction (up/down), and rates rather than raw counts. Producing a wall of numbers shows SQL skills but not yet analytical judgment. I bet Year-over-year growth would be useful as well. 

</details>

---

## You're a Data Detective Now. (Or A few more because the data now supports it)

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

Nov 29 drops to 0.54x baseline -- well below average despite 4x ad spend. Meanwhile, the days after (Nov 30 through Dec 2) surge to 1.36-1.57x. Cyber Monday (Dec 2) hits 1.57x. With 4x the normal ad budget, Black Friday should have been one of the biggest days of the year -- instead it was suppressed well below normal.

**Step 2: Discover the infrastructure table**

```sql
SELECT * FROM retaildb.main.dim_infrastructure ORDER BY valid_from;
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
FROM retaildb.main.dim_infrastructure
WHERE id = 'INFRA_0001'
ORDER BY valid_from;
```

INFRA_0001 went `degraded` on exactly 2024-11-29 (error_rate 0.25) and recovered on 2024-11-30. The timing matches perfectly -- the outage ate the expected Black Friday boost. Compare to the March outage (error_rate 0.35, activity dropped to 8.2% of prior day) and August outage (error_rate 0.4, dropped to 4.6%). The Black Friday outage was less severe (0.25 error rate), retaining 58.9% of prior day's activity, but still significantly suppressed what should have been a blockbuster day.

**Step 4 (thorough answer): Quantify all outage impacts**

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

</details>

<details>
<summary>Discussion</summary>

This exercise teaches root cause analysis. The business question is "what went wrong?" and the answer isn't in the customer data -- it's in an operational table you might not have noticed. This mirrors real analytics work: the explanation for a metric moving isn't always in the same table as the metric.

The dataset spans three years, so you can compare Black Friday across years (Nov 25 in 2022, Nov 24 in 2023, Nov 29 in 2024). In 2022 and 2023, Black Friday is among the highest-traffic days in its week. In 2024, it doesn't stand out at all -- Nov 30 and Dec 1-2 all surpass it. The cross-year comparison is stronger evidence than just looking at baseline multiples, because it controls for the holiday season effect.

The step-4 query reveals that the three outages had very different impacts -- March (error_rate 0.35) dropped activity to 8.2% of prior day, August (error_rate 0.4) to 4.6%, and November (error_rate 0.25) to 58.9% -- suggesting that error rate alone doesn't predict the severity of the impact; timing, baseline traffic volume, and day-of-week likely play a role. Even so, the November outage dragged Black Friday well below baseline (0.54x) despite 4x ad spend -- muting a potential blockbuster day into a below-average one.

Multiple levels of depth:

| Level | What you find |
|-------|--------------|
| Basic | "Nov 29 didn't spike like expected" (confirms the claim, stops there) |
| Moderate | Finds the infrastructure table, connects the outage to the date |
| Thorough | Quantifies all three outages, notices different severity levels across the three outages |
| Exceptional | Compares across years (2022/2023 BF clearly peaks, 2024 doesn't) and notes the post-outage surge (1.36-1.57x following days) suggests pent-up demand |

Follow-up questions to consider:
- "If you were the head of e-commerce, what would you recommend for next Black Friday?"
- "The system shows three outages in 2024. Is there a pattern?"
- "How would you estimate how much revenue the Black Friday outage cost?"

</details>

---

### Exercise 18: "Do bigger carts convert better?"

The VP of Sales saw the cart abandonment numbers from Exercise 7 and has a follow-up: "If someone loads up their cart with more items, are they more likely to actually buy? Or are the big carts the ones getting abandoned?"

<details>
<summary>Hints</summary>

- How do you measure "cart size"? Count of items, or total quantity?
- How do you know if a session converted? What's the signal?
- Is comparing averages enough, or should you look at the distribution?
- Could the number of *distinct products* in a cart matter more than total quantity?

</details>

<details>
<summary>Solution</summary>

**Compare cart quantity between converted and abandoned sessions:**

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

**Conversion rate by cart size bucket:**

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

</details>

<details>
<summary>Discussion</summary>

This exercise tests whether cart size predicts conversion. You should find that average cart quantity is virtually identical between converted and abandoned sessions (2.92 vs 2.90 items per session). The conversion rate across cart size buckets is also flat (8-10% across all buckets, from 1-item carts to 6+ items).

That's a real finding: bigger carts don't convert better in this data. In a real business, this would mean the VP's intuition ("big carts = serious buyers") isn't supported. The checkout friction affects all cart sizes equally.

A common mistake is conflating correlation with causation. Even if bigger carts *did* convert better, it wouldn't mean that encouraging larger carts would improve conversion -- it could just mean that more engaged customers both add more items and are more likely to buy.

</details>

---

### Exercise 19: "What's our average order value, and is it changing?"

The CFO wants a monthly AOV report. "I need to know what a typical order is worth, and whether it's trending up or down."

<details>
<summary>Hints</summary>

- What's the formula for order value when you have quantity and discounts?
- What defines an "order" -- a single purchase event, or all purchases in a session?
- How do you show a trend? Month-over-month change? A running average?
- What could make AOV change over time -- product mix? Discount levels? Customer mix?

</details>

<details>
<summary>Solution</summary>

**Monthly AOV with month-over-month change:**

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

</details>

<details>
<summary>Discussion</summary>

The revenue formula `price * quantity * (1 - discount_pct)` is deceptively simple but teaches an important concept: net revenue after discounts. Using `price` alone misses both quantity and discount effects.

AOV fluctuates month-to-month but shows no systematic trend. Month-over-month swings reflect changing product mix and order composition more than systematic trends.

If AOV is flat while order count grows, that's actually good news for the CFO -- the business is scaling without discounting more aggressively. If AOV were declining, the follow-up question would be "is it because we're discounting more, or because customers are buying cheaper products?"

The `LAG` window function is essential here. A table of absolute AOV numbers is hard to interpret -- the MoM percentage change immediately shows whether things are getting better or worse.

</details>

---

## Advanced

### Exercise 20: "Are discounts actually driving sales?"

Finance is reviewing the discount strategy. "We give discounts on a lot of purchases. Are they working? Do discounted orders have bigger baskets? Are certain customer segments getting more discounts than others?"

<details>
<summary>Hints</summary>

- How do you see the distribution of discount percentages? Think about bucketing/binning.
- Is the average discount the same across customer segments? Tiers?
- Do higher-discount purchases have more items (higher quantity)?
- What would it look like if discounts were completely random vs. strategically targeted?

</details>

<details>
<summary>Solution</summary>

**Discount distribution by customer segment:**

```sql
SELECT
    customer.segment,
    COUNT(*) AS purchases,
    ROUND(AVG(actions.discount_pct) * 100, 1) AS avg_discount_pct,
    ROUND(MIN(actions.discount_pct) * 100, 1) AS min_discount_pct,
    ROUND(MAX(actions.discount_pct) * 100, 1) AS max_discount_pct
FROM retaildb.main.fact_customer_action actions
INNER JOIN retaildb.main.dim_customer customer 
    ON actions.customer_id = customer.id AND customer.valid_to IS NULL
WHERE actions.action_type = 'purchase'
GROUP BY customer.segment
ORDER BY customer.segment;
```

**Discount buckets vs. basket size:**

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
    INNER JOIN retaildb.main.dim_product product 
        ON actions.product_id = product.id
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

</details>

<details>
<summary>Discussion</summary>

The key discovery: discounts appear uniformly distributed (0-15%) and completely independent of customer segment, tier, and basket size. Average discount is 7.5-7.6% for every segment. Budget customers get the same discounts as premium. Small baskets get the same discounts as large ones.

This is itself a finding -- and a valuable one. In real life, you'd report: "Our discounts aren't targeted. Every customer gets roughly the same discount regardless of who they are or how much they're buying. There's no evidence that discounts are driving larger baskets or being used strategically."

The recommendation writes itself: if the company wants discounts to drive behavior, they need to start targeting them. A uniform discount is indistinguishable from a price reduction.

Expectng to find a correlation? Here's an important lesson: **"no relationship" is a valid and important analytical finding.** Resist the urge to keep slicing the data until something looks significant.

</details>

---

### Exercise 21: "Which products do customers browse together?"

The merchandising team wants cross-sell recommendations. "If a customer is looking at Product A, what else should we recommend? Can we find natural product pairings from browsing behavior?"

<details>
<summary>Hints</summary>

- How do you find two products viewed in the same session?
- If you join a table to itself, how do you avoid pairing a product with itself?
- How do you avoid counting the pair (A, B) and (B, A) as two different pairs?
- Is product-level or category-level co-occurrence more useful?

</details>

<details>
<summary>Solution</summary>

**Category-level co-occurrence (more actionable):**

```sql
SELECT
    product1.category AS category_1,
    product2.category AS category_2,
    COUNT(DISTINCT action1.session_id) AS shared_sessions
FROM retaildb.main.fact_customer_action action1
INNER JOIN retaildb.main.fact_customer_action action2
    ON action1.session_id = action2.session_id
    AND action1.product_id <> action2.product_id
INNER JOIN retaildb.main.dim_product product1 
    ON action1.product_id = product1.id
    and product1.id is null
INNER JOIN retaildb.main.dim_product product2 
    ON action2.product_id = product2.id
    AND product2.id is null
WHERE 
    action1.action_type = 'product_view'
    AND action2.action_type = 'product_view'
    AND product1.category < product2.category
GROUP BY 
    product1.category, 
    product2.category
ORDER BY shared_sessions DESC;
```

**Product-level co-occurrence:**

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
INNER JOIN retaildb.main.dim_product product1 
    ON action1.product_id = product1.id
    AND product1.valid_to IS NULL
INNER JOIN retaildb.main.dim_product product2 
    ON action2.product_id = product2.id
    AND product2.valid_to IS NULL
WHERE action1.action_type = 'product_view'
  AND action2.action_type = 'product_view'
GROUP BY product1.name, product2.name, product1.category, product2.category
ORDER BY shared_sessions DESC
LIMIT 15;
```

In the product-level query, `action1.product_id < action2.product_id` prevents both self-pairs (A, A) and duplicate pairs ((A, B) and (B, A)). In the category-level query, we use `<>` for product IDs (to avoid excluding valid cross-category pairs) and `product1.category < product2.category` to deduplicate at the category level.

Note that dim_product is an SCD type 2. Though all products currently only have one row, we cannot guarantee no product changes will occur. That's why we ad `AND product1.valid_to IS NULL` and `AND product2.valid_to IS NULL`

</details>

<details>
<summary>Discussion</summary>

The category-level view is far more useful than product-level. Top co-browsed category pairs:

| category_1 | category_2 | shared_sessions |
|---|---|---:|
| accessories | smartphones | 5,038 |
| accessories | laptops | 4,213 |
| accessories | gaming | 3,628 |
| laptops | smartphones | 3,615 |
| gaming | smartphones | 3,055 |

Accessories appears in 3 of the top 5 pairs -- it's the universal cross-sell category. This makes business sense: people shopping for a laptop or phone naturally browse accessories too.

At the product level, the top pairs only share 28-42 sessions -- the signal is much weaker because products are more granular. (Note: this query groups by product name, not ID. Some product names map to multiple SKUs, so the true SKU-level co-browsing counts are lower.) This is a practical lesson: **aggregate before analyzing when individual-level data is too sparse for meaningful patterns.**

The self-join is the most important SQL concept here. The product-level query uses `action1.product_id < action2.product_id` to prevent self-pairs and duplicates -- it's elegant but not obvious. The category-level query uses `<>` instead of `<` for product IDs because `product_id` order doesn't correlate with category order; deduplication happens via `product1.category < product2.category`.

Follow-up questions:
- "Would you recommend accessories to someone browsing laptops, or laptops to someone browsing accessories? Does direction matter?"
- "How would you adapt this to find products that are *purchased* together, not just browsed together?"

</details>

---

## Digging Deeper, and Deeper, and Deeper

### Exercise 22: "Are we keeping customers, or just finding new ones?"

The head of growth is worried. "Our total customer count keeps going up, but I'm not sure if that's real growth or if we're just churning through people. Are customers coming back after their first visit?"

<details>
<summary>Hints</summary>

- How do you find each customer's first visit? What's their "cohort"?
- If you group customers by the month they first appeared, can you track how many return in later months?
- What's a good way to show retention over time -- absolute numbers or percentages?
- How do you handle cohorts that haven't had enough time to measure long-term retention?

</details>

<details>
<summary>Solution</summary>

**Cohort retention table:**

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
    INNER JOIN first_visit 
        ON actions.customer_id = first_visit.customer_id
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

**Aggregate retention curve:**

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
    INNER JOIN first_visit 
        ON actions.customer_id = first_visit.customer_id
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

</details>

<details>
<summary>Discussion</summary>

The retention picture is stark:

| Months since first visit | Retention |
|---:|---:|
| 0 | 100% |
| 1 | 5.1% |
| 3 | 4.7% |
| 6 | 4.1% |
| 12 | 2.7% |

There's a massive cliff from month 0 to month 1 -- ~95% of customers never return after their first month. After that initial drop, retention decays gradually, losing about 0.2 percentage points per month.

This answers the head of growth's question directly: **the business is heavily acquisition-dependent.** Growth is coming from finding new customers, not retaining existing ones. Only 5.1% return within a month, and by month 12, just 2.7% are still active.

Cohort-by-cohort, month-1 retention ranges from 3.0% to 9.9%, with no clear improving trend -- the company isn't getting better at retention over time. December cohorts are the largest (holiday traffic) but don't retain meaningfully better.

A notable pattern: once a customer returns after month 1, they tend to stay active for several more months. The challenge isn't keeping engaged customers -- it's getting first-time visitors to come back at all.

Multiple levels of depth:

| Level | What you build |
|-------|--------------|
| Basic | Month-1 retention percentage overall |
| Moderate | Full cohort table with multiple time horizons |
| Thorough | Aggregate retention curve + cohort-level comparison |
| Exceptional | Segment the cohort analysis by customer type (premium vs budget) to see if retention differs |

</details>

---
