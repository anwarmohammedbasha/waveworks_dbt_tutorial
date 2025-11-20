-- models/mart_customers_orders.sql
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
