# SQL Practice: Retail Analytics

23 SQL exercises using a simulated e-commerce dataset (TechMart Electronics). Exercises are framed as real business questions, progressing in difficulty.

## Setup

### DuckDB with Dbeaver (Recommended)

**Requires:** [DuckDB CLI](https://duckdb.org/docs/installation/)

**Option A: Build from CSV**

```bash
duckdb retaildb.duckdb < build_db.sql
```

**Option B: Download pre-built DB**

Download `retaildb.duckdb` from the [latest release](../../releases/latest).

### DBeaver

DBeaver is a free, open-source SQL editor. It is very popular and works well with DuckDB. 

[Dbeaver Instructions](https://duckdb.org/docs/stable/guides/sql_editors/dbeaver#:~:text=SQL%20Editors-,DBeaver%20SQL%20IDE,%2C%20then%20click%20%E2%80%9CFinish%E2%80%9D.)

### Roll Your Own

These exercises were tested on DuckDB and should work. Alternatively, feel free to import the CSVs into any DBMS you want. Some of the answers might need tweaking to work, but that's a good learning experience. 

## Usage

Open the database and start querying:

```bash
duckdb retaildb.duckdb # If you are a masochist
```

**DBeaver**

1. Database > New Database Connection
2. Select DuckDB
3. Browse to retaildb.duckdb
4. Play around. Explore



Exercises are in [exercises.md](exercises.md) -- each one includes collapsible hints, solutions, and discussion sections.

## Dataset

| Table | Rows | Description |
|-------|------|-------------|
| `dim_customer` | ~13K | Customer dimension (SCD-2) |
| `dim_product` | 203 | Product catalog |
| `dim_infrastructure` | 8 | System status (SCD-2) |
| `fact_customer_action` | ~246K | Customer actions (views, carts, purchases) |

~8,949 distinct customers across nearly three years (Mar 2022 -- Dec 2024). Generated with [Fabulexa](https://github.com/leoguerra97/fabulexa_sim).
