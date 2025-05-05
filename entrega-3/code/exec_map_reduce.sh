hdfs dfs -mkdir /data
hdfs dfs -put sw-script-e04.txt /data/
hadoop jar hadoop-3.3.6/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar \
wordcount /data/sw-script-e04.txt /data/sw-script-e04.wordcount
hadoop fs -cat /data/sw-script-e04.wordcount/part-r-00000 | more