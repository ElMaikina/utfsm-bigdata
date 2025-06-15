from pyspark.sql import SparkSession
from pyspark.sql.functions import col, floor, avg, count, sum as sum_, lit

# Inicializar Spark
spark = SparkSession.builder.getOrCreate()

# Parámetros
bucket = "204303630-inf356"
input_file = "vlt_observations_gc.parquet"
input_path = f"s3a://{bucket}/{input_file}"
output_file = input_file.replace(".parquet", ".count.parquet")
output_path = f"s3a://{bucket}/{output_file}"

# Leer archivo
df = spark.read.parquet(input_path)
print(f"Total registros cargados: {df.count()}")

# Asegurarse que las coordenadas están en float
df = df.withColumn("Galactic right ascension", col("Galactic right ascension").cast("float"))
df = df.withColumn("Galactic declination", col("Galactic declination").cast("float"))
df = df.withColumn("exposition_time", col("exposition_time").cast("float"))

# Crear segmentos de 10 grados
df = df.withColumn("ra_bin", floor(col("Galactic right ascension") / 10) * 10 + 5)  # Centro del bin
df = df.withColumn("dec_bin", floor(col("Galactic declination") / 10) * 10 + 5)

# Agrupar por bin e instrumento
df_grouped = df.groupBy("ra_bin", "dec_bin", "instrument").agg(
    count("*").alias("observation_count"),
    sum_("exposition_time").alias("total_exposition_time")
)

# Renombrar columnas para mayor claridad
df_grouped = df_grouped.withColumnRenamed("ra_bin", "Galactic right ascension") \
                       .withColumnRenamed("dec_bin", "Galactic declination")

# Guardar resultado
df_grouped.write.mode("overwrite").parquet(output_path)
print(f"Archivo guardado en: {output_path}")

# Detener Spark
spark.stop()