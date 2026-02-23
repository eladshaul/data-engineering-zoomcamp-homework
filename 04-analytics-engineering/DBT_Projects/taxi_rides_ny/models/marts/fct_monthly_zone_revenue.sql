with monthly_zone_revenue as(
select 
        service_type
       ,pickup_location_id 
       ,pickup_zone 
       ,extract(month from pickup_datetime) as pickup_month
       ,extract(year from pickup_datetime) as pickup_year
       ,sum(total_amount)total_amount
       
from {{ref("fct_trips")}}

group by 
        service_type
        ,pickup_location_id 
        ,pickup_zone 
        ,extract(month from pickup_datetime) 
        ,extract(year from pickup_datetime) 

order by 2,4,3
)
select * from monthly_zone_revenue