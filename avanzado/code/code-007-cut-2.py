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
# Toma una muestra de los anos para acelerar el proceso
df = df.sample(fraction=0.25, seed=3)
# Escribir archivo anuales
for year in df.select("adjusted_year").distinct().collect():
    y = year["adjusted_year"]
    df_year = df.filter(col("adjusted_year") == y).drop("first_lmonday", "year", "week")
    df_year.write.mode("overwrite").parquet(f"{output_root}/{y}/vlt_observations_{y}.parquet")
    # Subdivide por semana para agrupar anualmente
    df_weeks = df_year.withColumn("week", col("adjusted_week"))
    # Toma una muestra de las semanas para acelerar el proceso
    df_sample = df_weeks.sample(fraction=0.25, seed=3)
    for week in df_sample.select("week").distinct().collect():
        w = week["week"]
        df_w = df_sample.filter(col("week") == w)
        df_w.write.mode("overwrite").parquet(
            f"{output_root}/{y}/weeks/vlt_observations_{y}_{w}.parquet"
        )
        print(f"Final processed data for week {w} of the year {y}:")
        df_w.show(n=20)
# Detiene Spark
spark.stop()
