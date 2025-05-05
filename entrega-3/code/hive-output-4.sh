INFO  : No Stats for sw_dialogs@sw04_dialogs, Columns: character
INFO  : Semantic Analysis Completed (retrial = false)
INFO  : Created Hive schema: Schema(fieldSchemas:[FieldSchema(name:character, type:string, comment:null), FieldSchema(name:lines, type:bigint, comment:null)], properties:null)
INFO  : Completed compiling command(queryId=ubuntu_20250501025450_36332ece-1f44-45b7-998f-69c953bdb7af); Time taken: 3.888 seconds
INFO  : Concurrency mode is disabled, not creating a lock manager
INFO  : Executing command(queryId=ubuntu_20250501025450_36332ece-1f44-45b7-998f-69c953bdb7af): SELECT character, COUNT(*) AS lines
FROM sw04_dialogs
GROUP BY character
ORDER BY lines DESC
LIMIT 12
WARN  : Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. tez) or using Hive 1.X releases.
INFO  : Query ID = ubuntu_20250501025450_36332ece-1f44-45b7-998f-69c953bdb7af
INFO  : Total jobs = 2
INFO  : Launching Job 1 out of 2
INFO  : Starting task [Stage-1:MAPRED] in serial mode
INFO  : Number of reduce tasks not specified. Estimated from input data size: 1
INFO  : In order to change the average load for a reducer (in bytes):
INFO  :   set hive.exec.reducers.bytes.per.reducer=<number>
INFO  : In order to limit the maximum number of reducers:
INFO  :   set hive.exec.reducers.max=<number>
INFO  : In order to set a constant number of reducers:
INFO  :   set mapreduce.job.reduces=<number>
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
INFO  : number of splits:2
INFO  : Submitting tokens for job: job_1746065552179_0001
INFO  : Executing with tokens: []
printed operations logs
going to print operations logs
INFO  : The url to track the job: http://master:8088/proxy/application_1746065552179_0001/
INFO  : Starting Job = job_1746065552179_0001, Tracking URL = http://master:8088/proxy/application_1746065552179_0001/
INFO  : Kill Command = /home/ubuntu/hadoop-3.3.6/bin/mapred job  -kill job_1746065552179_0001
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs