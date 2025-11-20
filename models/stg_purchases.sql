-- models/stg_purchases.sql
{{ config(materialized='view') }}

select *
from {{ source('waveworks_raw', 'purchases') }}


