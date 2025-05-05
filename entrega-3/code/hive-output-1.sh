ubuntu@ip-172-31-30-146:~$ beeline -u "jdbc:hive2://localhost:10000/default;auth=noSasl" --verbose=true
!connect jdbc:hive2://localhost:10000/default;auth=noSasl '' [passwd stripped]
Connecting to jdbc:hive2://localhost:10000/default;auth=noSasl
Connected to: Apache Hive (version 4.0.1)
Driver: Hive JDBC (version 4.0.1)
Transaction isolation: TRANSACTION_REPEATABLE_READ
Beeline version 4.0.1 by Apache Hive
0: jdbc:hive2://localhost:10000/default> show databases;
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
printed operations logs
going to print operations logs
INFO  : Compiling command(queryId=ubuntu_20250501025436_a463ca5e-c723-4037-a672-4465e790fae9): show databases
INFO  : Semantic Analysis Completed (retrial = false)
INFO  : Created Hive schema: Schema(fieldSchemas:[FieldSchema(name:database_name, type:string, comment:from deserializer)], properties:null)
INFO  : Completed compiling command(queryId=ubuntu_20250501025436_a463ca5e-c723-4037-a672-4465e790fae9); Time taken: 2.378 seconds
INFO  : Concurrency mode is disabled, not creating a lock manager
INFO  : Executing command(queryId=ubuntu_20250501025436_a463ca5e-c723-4037-a672-4465e790fae9): show databases
INFO  : Starting task [Stage-0:DDL] in serial mode
INFO  : Completed executing command(queryId=ubuntu_20250501025436_a463ca5e-c723-4037-a672-4465e790fae9); Time taken: 0.217 seconds
printed operations logs
Getting log thread is interrupted, since query is done!
+----------------+
| database_name  |
+----------------+
| default        |
+----------------+
1 row selected (3.366 seconds)
0: jdbc:hive2://localhost:10000/default> !run hive-script.hql
>>>  CREATE DATABASE sw_dialogs;
going to print operations logs
printed operations logs
Getting log thread is interrupted, since query is done!
INFO  : Compiling command(queryId=ubuntu_20250501025448_df7a8fbc-1987-45fb-ad48-d61a6bb732a5): CREATE DATABASE sw_dialogs
INFO  : Semantic Analysis Completed (retrial = false)
INFO  : Created Hive schema: Schema(fieldSchemas:null, properties:null)
INFO  : Completed compiling command(queryId=ubuntu_20250501025448_df7a8fbc-1987-45fb-ad48-d61a6bb732a5); Time taken: 0.009 seconds
INFO  : Concurrency mode is disabled, not creating a lock manager
INFO  : Executing command(queryId=ubuntu_20250501025448_df7a8fbc-1987-45fb-ad48-d61a6bb732a5): CREATE DATABASE sw_dialogs
INFO  : Starting task [Stage-0:DDL] in serial mode
INFO  : Completed executing command(queryId=ubuntu_20250501025448_df7a8fbc-1987-45fb-ad48-d61a6bb732a5); Time taken: 0.224 seconds
No rows affected (0.253 seconds)
>>>
>>>  USE sw_dialogs;
going to print operations logs
printed operations logs