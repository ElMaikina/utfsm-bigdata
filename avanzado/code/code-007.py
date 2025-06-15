from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_unixtime, to_date, date_format, unix_timestamp, expr, floor, min
)
from pyspark.sql.window import Window

# Crear sesión Spark
spark = SparkSession.builder.getOrCreate()

# Parámetros de entrada/salida
bucket = "204303630-inf356"
input_path = f"s3a://{bucket}/vlt_observations_gc.parquet"
output_root = f"s3a://{bucket}/partition"

# Leer el archivo con coordenadas galácticas
df = spark.read.parquet(input_path)

# Convertir "Template start" (UNIX timestamp) a fecha
df = df.withColumn("obs_date", to_date(from_unixtime(col("template_start_unix"))))

# Calcular primer lunes del año para cada año presente
years_df = df.selectExpr("year(obs_date) as year").distinct()
years_df = years_df.withColumn(
    "first_lmonday",
    expr("""
        next_day(to_date(concat(year, '-01-01')), 'Monday')
    """)
)

# Asociar a cada fila su primer lunes del año correspondiente
df = df.withColumn("year", expr("year(obs_date)"))
df = df.join(years_df, on="year", how="left")

# Calcular semana desde el primer lunes (inicio de semana 0)
df = df.withColumn(
    "week",
    floor(
        (unix_timestamp(col("obs_date")) - unix_timestamp(col("first_lmonday")))
        / (86400 * 7)
    )
)

# Reasignar a año anterior si la fecha es antes del primer lunes
df = df.withColumn(
    "adjusted_year",
    expr("IF(obs_date < first_lmonday, year - 1, year)")
).withColumn(
    "adjusted_week",
    expr("IF(obs_date < first_lmonday, 0, week)")
)

# Escribir archivo por año (todos los datos de ese año)
for year in df.select("adjusted_year").distinct().collect():
    y = year["adjusted_year"]
    df_year = df.filter(col("adjusted_year") == y).drop("first_lmonday", "year", "week")
    df_year.write.mode("overwrite").parquet(f"{output_root}/{y}/vlt_observations_{y}.parquet")

    # Subdividir por semana
    df_weeks = df_year.withColumn("week", col("adjusted_week"))
    for week in df_weeks.select("week").distinct().collect():
        w = week["week"]
        df_w = df_weeks.filter(col("week") == w)
        df_w.write.mode("overwrite").parquet(
            f"{output_root}/{y}/weeks/vlt_observations_{y}_{w}.parquet"
        )

# Finalizar sesión
spark.stop()
