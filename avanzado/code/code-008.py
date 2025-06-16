from pyspark.sql import SparkSession
from pyspark.sql.functions import col, floor, avg, count, sum as sum_, lit


# Bucket personal
bucket = "204303630-inf356"

# Direccion de entrada
input_file = "vlt_observations_gc.parquet"
input_path = f"s3a://{bucket}/{input_file}"

# Direccion de la salida
output_file = input_file.replace(".parquet", ".count.parquet")
output_path = f"s3a://{bucket}/{output_file}"

# Iniciar Spark
spark = SparkSession.builder.getOrCreate()

# Leer archivo
df = spark.read.parquet(input_path)
print(f"Total registers loaded: {df.count()}")

# Asegurarse que las coordenadas están en float
df = df.withColumn("gal_ra", col("gal_ra").cast("float"))
df = df.withColumn("gal_dec", col("gal_dec").cast("float"))
df = df.withColumn("exposition_time", col("exposition_time").cast("float"))

# Crear segmentos de 10 grados
df = df.withColumn("ra_bin", floor(col("gal_ra") / 10) * 10 + 5)  # Centro del bin
df = df.withColumn("dec_bin", floor(col("gal_dec") / 10) * 10 + 5)

# Agrupar por bin e instrumento
df_grouped = df.groupBy("ra_bin", "dec_bin", "instrument").agg(
    count("*").alias("observation_count"),
    sum_("exposition_time").alias("total_exposition_time")
)

# Renombrar columnas para mayor claridad
df_grouped = df_grouped.withColumnRenamed("ra_bin", "gal_ra") \
                       .withColumnRenamed("dec_bin", "gal_dec")

# Guardar resultado
print(f"Attempting to save processed data to '{output_path}'...")
df_grouped.write.mode("overwrite").parquet(output_path)
print(f"Succesfully saved processed data to '{output_path}'!")

# Muestra las filas procesadas
print(f"Final processed rows: {df_grouped}")
print(f"Final rows extracted: {df_grouped.count()}")
print(f"Final processed data:")
df_grouped.show(n=20)

# Detener Spark
spark.stop()