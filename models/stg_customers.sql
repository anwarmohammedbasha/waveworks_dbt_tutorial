-- models/stg_customers.sql
{{ config(materialized='view') }}

select *
from { source('waveworks_raw', 'customers') }
