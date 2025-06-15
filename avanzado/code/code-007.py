from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date, date_format, unix_timestamp, expr, floor, min
from pyspark.sql.window import Window

# Bucket personal
bucket = "204303630-inf356"

# Iniciar Spark
spark = SparkSession.builder.getOrCreate()

# Direccion de la entrada
input_path = f"s3a://{bucket}/vlt_observations_gc.parquet"

# Direccion de la salida
output_root = f"s3a://{bucket}/partition"

# Lee el archivo con coordenadas galácticas
df = spark.read.parquet(input_path)

# Conveierte la fecha unix a fecha date
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

# Calcula la semana desde el primer lunes
df = df.withColumn(
    "week",
    floor(
        (unix_timestamp(col("obs_date")) - unix_timestamp(col("first_lmonday")))
        / (86400 * 7)
    )
)
print(f"Calculating weeks since first monday of the year: {df}")

# Ajusta al anterior anterior si la fecha es antes del primer lunes
df = df.withColumn(
    "adjusted_year",
    expr("IF(obs_date < first_lmonday, year - 1, year)")
).withColumn(
    "adjusted_week",
    expr("IF(obs_date < first_lmonday, 0, week)")
)
print(f"Adding days before the first monday to the year before: {df}")

# Escribir archivo anuales
for year in df.select("adjusted_year").distinct().collect():
    y = year["adjusted_year"]
    df_year = df.filter(col("adjusted_year") == y).drop("first_lmonday", "year", "week")
    df_year.write.mode("overwrite").parquet(f"{output_root}/{y}/vlt_observations_{y}.parquet")
    print(f"Final processed data for each year: {df_year}")

    # Subdivide por semana
    df_weeks = df_year.withColumn("week", col("adjusted_week"))
    for week in df_weeks.select("week").distinct().collect():
        w = week["week"]
        df_w = df_weeks.filter(col("week") == w)
        df_w.write.mode("overwrite").parquet(
            f"{output_root}/{y}/weeks/vlt_observations_{y}_{w}.parquet"
        )
        print(f"Final processed data for each week: {df_w}")

# Detiene Spark
spark.stop()
