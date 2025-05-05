# hadoop-3.3.6/etc/hadoop/mapred-site.xml
<property>
    <name>mapreduce.job.running.map.limit</name>
    <value>8</value> # Modificar de 4 a 8
</property>
# ...
<property>
<name>mapreduce.job.reduces</name>
    <value>8</value> # Modificar de 4 a 8
</property>
# ...
<property>
    <name>mapreduce.job.running.reduce.limit</name>
    <value>8</value> # Modificar de 4 a 8
</property>

# hadoop-3.3.6/etc/hadoop/workers
172.31.30.0
172.31.17.157
172.31.24.51
172.31.27.79
172.31.84.79
172.31.93.162
172.31.92.28
172.31.81.101

# /home/ubuntu/install.sh
# WORKERS=("172.31.30.0" "172.31.17.157" "172.31.24.51" "172.31.27.79")
WORKERS=("172.31.30.0" "172.31.17.157" "172.31.24.51" "172.31.27.79"  \
"172.31.84.79" "172.31.93.162" "172.31.92.28" "172.31.81.101")
MASTER="172.31.30.146"