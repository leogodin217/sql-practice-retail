-- Build retaildb.duckdb from CSV files
-- Usage: duckdb retaildb.duckdb < build_db.sql

CREATE TABLE dim_customer AS
SELECT
    id, name, email, username, phone,
    street_address, city, state, zip_code,
    birth_date::DATE AS birth_date,
    age::INTEGER AS age,
    income::DOUBLE AS income,
    segment, tier,
    total_purchases::INTEGER AS total_purchases,
    acquisition_source,
    valid_from::TIMESTAMP AS valid_from,
    valid_to::TIMESTAMP AS valid_to,
    active::BOOLEAN AS active
FROM read_csv('data/dim_customer.csv', header=true, auto_detect=true);

CREATE TABLE dim_product AS
SELECT
    id, name, category,
    price::INTEGER AS price,
    popularity::DOUBLE AS popularity,
    margin::DOUBLE AS margin,
    in_stock::BOOLEAN AS in_stock,
    valid_from::TIMESTAMP AS valid_from,
    valid_to::TIMESTAMP AS valid_to
FROM read_csv('data/dim_product.csv', header=true, auto_detect=true);

CREATE TABLE dim_infrastructure AS
SELECT
    id, status, primary_ip, domain,
    error_rate::DOUBLE AS error_rate,
    valid_from::TIMESTAMP AS valid_from,
    valid_to::TIMESTAMP AS valid_to
FROM read_csv('data/dim_infrastructure.csv', header=true, auto_detect=true);

CREATE TABLE fact_customer_action AS
SELECT
    action_id::INTEGER AS action_id,
    timestamp::TIMESTAMP AS timestamp,
    customer_id, product_id, action_type,
    action_sequence::INTEGER AS action_sequence,
    session_id, funnel_stage,
    quantity::INTEGER AS quantity,
    discount_pct::DOUBLE AS discount_pct
FROM read_csv('data/fact_customer_action.csv', header=true, auto_detect=true);
