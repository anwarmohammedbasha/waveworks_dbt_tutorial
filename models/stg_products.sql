-- models/stg_products.sql
{{ config(materialized='view') }}

select *
from {{ source('waveworks_raw', 'products') }}


