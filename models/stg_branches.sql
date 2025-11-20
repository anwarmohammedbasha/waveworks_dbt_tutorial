-- models/stg_branches.sql
{{ config(materialized='view') }}

select *
from {{ source('waveworks_raw', 'branches') }}


