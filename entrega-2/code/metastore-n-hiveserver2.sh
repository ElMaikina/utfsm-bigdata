# Levanta ambos servicios en segundo plano y esconde su salida
nohup hive --service hiveserver2 > /dev/null 2>&1
nohup hive --service metastore > /dev/null 2>&1