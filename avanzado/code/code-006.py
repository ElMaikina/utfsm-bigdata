from pyspark.sql import SparkSession
from pyspark.sql.functions import col, radians, degrees, cos, sin, atan2, asin

# Load parquet from previous ETL step
bucket = "204303630-inf356"

# Iniciar Spark
spark = SparkSession.builder.getOrCreate()

# Direccion de la entrada
input_path = f"s3a://{bucket}/vlt_observations_etl.parquet"

# Lee y guarda la entrada en un dataframe
df = spark.read.parquet(input_path)

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

# Calcula las coordenadas galacticas
df = df.withColumn("x_gal", 
    -0.05487556 * col("x_eq") +
    -0.87343709 * col("y_eq") +
    -0.48383502 * col("z_eq")
).withColumn("y_gal", 
     0.49410943 * col("x_eq") +
    -0.44482963 * col("y_eq") +
     0.74698225 * col("z_eq")
).withColumn("z_gal", 
    -0.86766615 * col("x_eq") +
    -0.19807637 * col("y_eq") +
     0.45598378 * col("z_eq")
)

# Devuelve las coordenadas a esfericas
df = df.withColumn("gal_ra", (degrees(atan2(col("y_gal"), col("x_gal"))) + 360) % 360)
df = df.withColumn("gal_dec", degrees(asin(col("z_gal"))))

# Toma sola las columnas deseadas
df_final = df.select(
    col("gal_ra"),
    col("gal_dec"),
    col("instrument"),
    col("exposition_time"),
    col("template_start_unix")
)

# Guarda el dataframe como parquet
output_path = f"s3a://{bucket}/vlt_observations_gc.parquet"
df_final.write.mode("overwrite").parquet(output_path)

# Muestra las filas procesadas
print(f"Final processed rows: {df_final}")
print(f"Final rows extracted: {df_final.count()}")
print(f"Final processed data:")
df_final.show(n=20)

# Detiene Spark
spark.stop()