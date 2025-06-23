from pyspark.sql import SparkSession
from pyspark.sql.functions import col, radians, degrees, cos, sin, atan2, asin
# Bucket personal
bucket = "204303630-inf356"
# Direccion de entrada
input_path = f"s3a://{bucket}/vlt_observations_etl.parquet"
# Direccion de salida
output_path = f"s3a://{bucket}/vlt_observations_gc.parquet"
# Iniciar Spark
spark = SparkSession.builder.getOrCreate()
# Lee y guarda la entrada en un dataframe
df = spark.read.parquet(input_path)
# Toma una muestra de los anos para acelerar el proceso
df = df.sample(fraction=0.25, seed=3)
# Transforma los datos a radianes
df = df.withColumn("ra_rad", radians(
    col("ra_deg") +
    col("ra_min") / 60 +
    col("ra_sec") / 3600
)).withColumn("dec_rad", radians(
    col("dec_deg") +
    col("dec_min") / 60 +
    col("dec_sec") / 3600
))
# Calcula las coordenadas cartesianas
df = df.withColumn("x_eq", cos(col("dec_rad")) * cos(col("ra_rad")))
df = df.withColumn("y_eq", cos(col("dec_rad")) * sin(col("ra_rad")))
df = df.withColumn("z_eq", sin(col("dec_rad")))