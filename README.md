# SQL Practice: Retail Analytics

22 SQL exercises using a simulated e-commerce dataset (TechMart Electronics). Exercises are framed as real business questions, progressing in difficulty from beginner to intermmediate.  

## Why? 

Look. Leetcode, Datalemur etc. are great resources, but they leave a gap. With so much focus on syntax and well-defined problems, they don't teach you to analyze a database, think about the bigger picture, or think creatively. In the real world problems come in as vague questions that are often open to interpretation. There isn't always a right answer. At work, we generally interact with one or a few databases over and over. We learn them over time. What we do on the easy stuff gives us more understanding when the harder stuff comes along.  

These practice exercises are framed as business scenarios that require you to make decisions. Define terms. Understand what data could answer the question. And while I do provide potential answers, some have no single right answer. Getting the right answer is less important than the process you use to define the problem and come up with good solutions. 

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
| `dim_customer` | 13,294 | Customer dimension (SCD-2) |
| `dim_product` | 203 | Product catalog |
| `dim_infrastructure` | 8 | System status (SCD-2) |
| `fact_customer_action` | 242,618 | Customer actions (views, carts, purchases) |

9,074 distinct customers across nearly three years (Mar 2022 -- Dec 2024). Generated with Fabulexa (A configurable synthetic data generator)

## Use of AI

I use LLMs every day. At work. At home. AI is integrated in my workflows and this project is no different. This is how I built these practice exercises.  

1. I used Claude Code to build a configurable synthetic data generator. (Took eight months and many failed experiments)
2. Used Claude to vet my idea for good practice exercises. Vague questions. Business scenarios. All on the same database. Hints. Etc. 
3. Back and forth with Claude until it understood exactly what I wanted. 
4. Let Claude generate the dataset, questions and queries.
5. Reviewed, analyzed, and iterated until I got exactly what I wanted. 
6. Hand edited the rest. 

## What's Next

Hmm. Definitely getting back to the SQL course *Intuitive SQL from 0 to Dangerous* that I started eight months ago. I can generate databases and exercies really fast now, so more repos like this one. Maybe adding LLM instructions for helping people through the exercises would be good. Something where you could use an LLM to help you through the exercises without just giving answers. Make it more of a learning experience than just practice. 