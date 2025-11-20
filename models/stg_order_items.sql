-- models/stg_order_items.sql
{{ config(materialized='view') }}

select *
from { source('waveworks_raw', 'order_items') }
