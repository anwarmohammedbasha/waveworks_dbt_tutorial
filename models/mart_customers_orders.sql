-- models/mart_customers_orders.sql
{{ config(materialized='table') }}

with customers as (
  select * from { ref('stg_customers') }
)
-- if an orders table exists, attempt join

, orders as (
  select * from { ref('stg_orders') }
)

select
  c.*,
  count(o.*) as orders_count
from customers c
left join orders o on o.customer_id = c.id
group by c.id
