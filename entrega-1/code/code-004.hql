CREATE DATABASE sw_dialogs;
 
USE sw_dialogs;
 
CREATE TABLE sw04_dialogs (
  line      INT,
  character STRING,
  dialog    STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = " ",
  "quoteChar" = "\""
)
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");
 
LOAD DATA INPATH
'/data/sw-script-e04.txt'
INTO TABLE
sw04_dialogs;
 
SELECT character, COUNT(*) AS lines
FROM sw04_dialogs
GROUP BY character
ORDER BY lines DESC
LIMIT 12;
