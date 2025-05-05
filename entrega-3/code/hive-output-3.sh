No rows affected (0.866 seconds)
>>>
>>>  LOAD DATA INPATH
'/data/sw-script-e04.txt'
INTO TABLE
sw04_dialogs;
going to print operations logs
printed operations logs
going to print operations logs
INFO  : Compiling command(queryId=ubuntu_20250501025449_c327dfb8-5749-408f-b787-70bc8925a884): LOAD DATA INPATH
'/data/sw-script-e04.txt'
INTO TABLE
sw04_dialogs
INFO  : Semantic Analysis Completed (retrial = false)
INFO  : Created Hive schema: Schema(fieldSchemas:null, properties:null)
INFO  : Completed compiling command(queryId=ubuntu_20250501025449_c327dfb8-5749-408f-b787-70bc8925a884); Time taken: 0.406 seconds
INFO  : Concurrency mode is disabled, not creating a lock manager
INFO  : Executing command(queryId=ubuntu_20250501025449_c327dfb8-5749-408f-b787-70bc8925a884): LOAD DATA INPATH
'/data/sw-script-e04.txt'
INTO TABLE
sw04_dialogs
INFO  : Starting task [Stage-0:MOVE] in serial mode
INFO  : Loading data to table sw_dialogs.sw04_dialogs from hdfs://172.31.30.146/data/sw-script-e04.txt
INFO  : Starting task [Stage-1:STATS] in serial mode
INFO  : Executing stats task
INFO  : Table sw_dialogs.sw04_dialogs stats: [numFiles=2, totalSize=156556, numFilesErasureCoded=0]
INFO  : Completed executing command(queryId=ubuntu_20250501025449_c327dfb8-5749-408f-b787-70bc8925a884); Time taken: 0.866 seconds
printed operations logs
Getting log thread is interrupted, since query is done!
No rows affected (1.308 seconds)
>>>
>>>  SELECT character, COUNT(*) AS lines
FROM sw04_dialogs
GROUP BY character
ORDER BY lines DESC
LIMIT 12;
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
INFO  : Compiling command(queryId=ubuntu_20250501025450_36332ece-1f44-45b7-998f-69c953bdb7af): SELECT character, COUNT(*) AS lines
FROM sw04_dialogs
GROUP BY character
ORDER BY lines DESC
LIMIT 12