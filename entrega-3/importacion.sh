# Campos que tendra el archivo. Como desconocemos el contenido, le asignamos parametros genericos

# Exportamos cada linea del Script de manera dinamica
echo "CREATE DATABASE dirty_database;" > dirty_data_script.hql
echo "USE dirty_database;" >> dirty_data_script.hql
echo "CREATE TABLE dirty_table (" >> dirty_data_script.hql

# Obtenemos la cantidad de parametros extrayendo una fila aleatoria del archivo
# al que posteriormente se le remplazaron las comas por saltos de linea
grep -Eo "," vlt_observations_000_single_row.csv > comas
N_OF_PARAMS=$(wc -l < comas)

# Contador para nombrar cada parametro
COUNTER=0

# Guarda cada parametro generico como un String, posteriormente los
# segregaremos en base a las salidas que nos dan las Querys de esta
# Base de Datos Generica
while [ "$COUNTER" -le "$N_OF_PARAMS" ]; do
    echo "      parametro_$COUNTER string," >> dirty_data_script.hql
        COUNTER=$((COUNTER+1))
done

# Quitar la ultima Coma que queda molestando
truncate -s-2 dirty_data_script.hql

echo " )" >> dirty_data_script.hql
echo "COMMENT 'Datos Genericos'" >> dirty_data_script.hql
echo "ROW FORMAT DELIMITED" >> dirty_data_script.hql
echo "FIELDS TERMINATED BY ',';" >> dirty_data_script.hql

# Finalmente cargamos el CSV en nuestro HDFS para rellenar los datos
echo "LOAD DATA INPATH '/data/vlt_observations_000.csv' INTO TABLE vlt_obs_generic;" >> dirty_data_script.hql

# Subir el archivo a nuestro DFS
hdfs dfs -put vlt_observations_000.csv /data/