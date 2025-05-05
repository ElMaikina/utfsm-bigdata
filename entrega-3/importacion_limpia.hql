CREATE DATABASE dirty_database;
USE dirty_database;
CREATE TABLE clean_table (
        parametro_0 string,
        parametro_1 string,
        parametro_2 string,
        ...
        parametro_30 string,
        parametro_31 string,
        parametro_32 string
)
COMMENT 'Datos Genericos'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';
LOAD DATA INPATH '/data/vlt_observations_000_clean.csv' INTO TABLE clean_table;