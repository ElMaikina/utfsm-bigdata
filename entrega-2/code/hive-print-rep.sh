#!/bin/bash
HDFS_FILE="/user/hive/warehouse/sw_dialogs.db/sw04_dialogs/sw-script-e04.txt"

hdfs fsck $HDFS_FILE -files -blocks -locations > fsck_output

grep -o '[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*' fsck_output.txt > IP_with_Star_Wars.txt
grep -o 'blk_[0-9]*_[0-9]*' fsck_output.txt > Blocks_with_Star_Wars.txt
grep "Average block replication:" fsck_output.txt | grep -o "[0-9\.]*" > Rep_Fact_Star_Wars.txt

BLOCKS_QTY="$(wc -l Blocks_with_Star_Wars.txt | grep -o '[0-9]*')"
AVG_REP="$(cat Rep_Fact_Star_Wars.txt)"

COUNTER=0

echo "File: $HDFS_FILE"
echo "Blocks: $BLOCKS_QTY"
echo "Avg. Replication: $AVG_REP"

cat Blocks_with_Star_Wars.txt | while read line
do
    echo "$COUNTER - $line - $(cat Blocks_with_Star_Wars.txt)"
    ((counter++))
done