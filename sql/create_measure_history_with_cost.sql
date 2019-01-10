drop table if exists measure_history ;

create table measure_history(
  measure_history_id integer primary key autoincrement
, measure_time timestamp not null default current_timestamp
, sensor_count_1 INTEGER
, sensor_count_2 INTEGER
, sensor_1_rate_mwh INTEGER
, sensor_2_rate_mwh INTEGER
, sensor_temp
, sensor_hum
, sensor_1_rate_cost INTEGER
, sensor_2_rate_cost INTEGER
, total_cost INTEGER
);

drop table if exists totals ;

create table totals(
  totals_id integer primary key autoincrement
, measure_time1 timestamp not null default current_timestamp
, sensor_1_total_cost integer
, sensor_2_total_cost integer
, combined_total_cost INTEGER
);
