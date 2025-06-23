from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date, date_format, unix_timestamp, expr, floor, min
from pyspark.sql.window import Window
# Bucket personal
bucket = "204303630-inf356"
# Direccion de entrada
input_path = f"s3a://{bucket}/vlt_observations_gc.parquet"
# Direccion de la salida
output_root = f"s3a://{bucket}/partition"
# Iniciar Spark
spark = SparkSession.builder.getOrCreate()
# Lee el archivo con coordenadas galácticas
df = spark.read.parquet(input_path)
# Convierte la fecha unix a fecha date
df = df.withColumn("obs_date", to_date(from_unixtime(col("template_start_unix"))))
# Calcula el primer lunes anual
years_df = df.selectExpr("year(obs_date) as year").distinct()
print(f"All distinct years read from data: {years_df}")
years_df = years_df.withColumn(
    "first_lmonday",
    expr("""
        next_day(to_date(concat(year, '-01-01')), 'Monday')
    """)
)
print(f"Adding column to data for the first monday of the year: {years_df}")
# Asocia cada fila al primer lunes anual
df = df.withColumn("year", expr("year(obs_date)"))
print(f"Adding new column for the year: {df}")
df = df.join(years_df, on="year", how="left")
print(f"Associate each row to first year monday: {df}")