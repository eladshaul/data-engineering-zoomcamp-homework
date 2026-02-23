with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),
renamed as (
    select
        -- identifiers
        dispatching_base_num,
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropOff_datetime as timestamp) as dropOff_datetime,
        cast(PUlocationID as integer) as pickup_location_id,
        cast(DOlocationID as integer) as dropoff_location_id,
        SR_Flag,	
        Affiliated_base_number

    from source
    where extract(year from pickup_datetime) = 2019
    and dispatching_base_num IS not NULL
)

select * from renamed
