CREATE DATABASE dirty_database;
USE dirty_database;
CREATE TABLE dirty_table (
        parametro_0 string,
        parametro_1 string,
        parametro_2 string,
        parametro_3 string,
        parametro_4 string,
        parametro_5 string,
        parametro_6 string,
        parametro_7 string,
        parametro_8 string,
        parametro_9 string,
        parametro_10 string,
        parametro_11 string,
        parametro_12 string,
        parametro_13 string,
        parametro_14 string,
        parametro_15 string,
        parametro_16 string,
        parametro_17 string,
        parametro_18 string,
        parametro_19 string,
        parametro_20 string,
        parametro_21 string,
        parametro_22 string,
        parametro_23 string,
        parametro_24 string,
        parametro_25 string,
        parametro_26 string,
        parametro_27 string,
        parametro_28 string,
        parametro_29 string,
        parametro_30 string,
        parametro_31 string,
        parametro_32 string
)
COMMENT 'Datos Genericos'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';
LOAD DATA INPATH '/data/vlt_observations_000.csv' INTO TABLE dirty_table;