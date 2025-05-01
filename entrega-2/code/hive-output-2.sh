Getting log thread is interrupted, since query is done!
INFO  : Compiling command(queryId=ubuntu_20250501025448_a7a58e45-3065-4b8d-987f-382f6be6ac0d): USE sw_dialogs
INFO  : Semantic Analysis Completed (retrial = false)
INFO  : Created Hive schema: Schema(fieldSchemas:null, properties:null)
INFO  : Completed compiling command(queryId=ubuntu_20250501025448_a7a58e45-3065-4b8d-987f-382f6be6ac0d); Time taken: 0.026 seconds
INFO  : Concurrency mode is disabled, not creating a lock manager
INFO  : Executing command(queryId=ubuntu_20250501025448_a7a58e45-3065-4b8d-987f-382f6be6ac0d): USE sw_dialogs
INFO  : Starting task [Stage-0:DDL] in serial mode
INFO  : Completed executing command(queryId=ubuntu_20250501025448_a7a58e45-3065-4b8d-987f-382f6be6ac0d); Time taken: 0.041 seconds
No rows affected (0.108 seconds)
>>>
>>>  CREATE TABLE sw04_dialogs (
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
going to print operations logs
printed operations logs
Getting log thread is interrupted, since query is done!
INFO  : Compiling command(queryId=ubuntu_20250501025448_7e5cb1f6-8c26-4e7c-aa1e-7a905630ea48): CREATE TABLE sw04_dialogs (
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
TBLPROPERTIES ("skip.header.line.count"="1")
INFO  : Semantic Analysis Completed (retrial = false)
INFO  : Created Hive schema: Schema(fieldSchemas:null, properties:null)
INFO  : Completed compiling command(queryId=ubuntu_20250501025448_7e5cb1f6-8c26-4e7c-aa1e-7a905630ea48); Time taken: 0.102 seconds
INFO  : Concurrency mode is disabled, not creating a lock manager
INFO  : Executing command(queryId=ubuntu_20250501025448_7e5cb1f6-8c26-4e7c-aa1e-7a905630ea48): CREATE TABLE sw04_dialogs (
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
TBLPROPERTIES ("skip.header.line.count"="1")
INFO  : Starting task [Stage-0:DDL] in serial mode
INFO  : Completed executing command(queryId=ubuntu_20250501025448_7e5cb1f6-8c26-4e7c-aa1e-7a905630ea48); Time taken: 0.724 seconds