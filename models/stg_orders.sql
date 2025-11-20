-- models/stg_orders.sql
{{ config(materialized='view') }}

select *
from {{ source('waveworks_raw', 'orders') }}


