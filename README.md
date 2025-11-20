# 🚀 Waveworks dbt + DuckDB Project

A simple beginner-friendly **dbt (data build tool)** project using **DuckDB** as the analytical database.
This project transforms raw Waveworks data into clean staging models and a final customer analytics mart.

---

## 📘 Overview

This project demonstrates:

* Setting up **dbt with DuckDB**
* Creating **staging models** from raw tables
* Creating a **mart model** for analytics
* Running dbt locally
* Understanding dbt folder structure

---

## 📁 Project Structure

```
.
├── models/
│   ├── staging/
│   │   ├── stg_branches.sql
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   ├── stg_order_items.sql
│   │   ├── stg_products.sql
│   │   └── stg_purchases.sql
│   ├── mart_customers_orders.sql
│   └── schema.yml
│
├── data/
│   └── waveworks.duckdb
│
├── dbt_project.yml
└── README.md
```

---

## 🧠 Final Model: `mart_customers_orders`

This model aggregates customer behavior and order patterns.

### Columns included:

* `customer_key`
* `name`
* `channel`
* `orders_count`
* `first_order_at`
* `last_order_at`
* `total_spend`

### SQL:

```sql
{{ config(materialized='table') }}

select
  c.customer_id as customer_key,
  c.name,
  c.channel,
  count(o.order_id) as orders_count,
  min(o.order_datetime) as first_order_at,
  max(o.order_datetime) as last_order_at,
  sum(o.total_amount) as total_spend
from {{ ref('stg_customers') }} as c
left join {{ ref('stg_orders') }} as o
  on o.customer_id = c.customer_id
group by
  c.customer_id,
  c.name,
  c.channel
```

---

## ▶️ How to Run

### 1️⃣ Create virtual environment

```
python -m venv .venv
```

### 2️⃣ Activate it

```
.venv\Scripts\activate   # Windows
```

### 3️⃣ Install dbt

```
pip install dbt-core dbt-duckdb
```

### 4️⃣ Run dbt

```
dbt debug
dbt clean
dbt run
dbt test
```

---

## 🧪 Testing

Run model tests:

```
dbt test
```

---

## 📝 Blog Article

Full walkthrough available here:

👉 **[https://medium.com/@anwarmohammedbasha/getting-started-with-dbt-using-duckdb-3c6e0de774ae](https://medium.com/@anwarmohammedbasha/getting-started-with-dbt-using-duckdb-3c6e0de774ae)**

