select
datetime(measure_time, '+10 hours') as measure_time
, sensor_count_1 
, sensor_count_2 
, sensor_count_1 + sensor_count_2 as sensor_count_total
, sensor_1_rate_mwh
, sensor_2_rate_mwh
, sensor_1_rate_mwh + sensor_2_rate_mwh as sensor_rate_mwh_total
, printf("%.1f", temperature) as temperature
, printf("%.1f", humidity) as humidity
, sensor_1_rate_cost
, sensor_2_rate_cost
, total_cost
from measure_history
order by measure_time desc;

select 
 datetime(measure_time1, '+10 hours') as measure_time1
, sensor_1_total_cost
, sensor_2_total_cost
, combined_total_cost
from totals
order by measure_time1 desc;
