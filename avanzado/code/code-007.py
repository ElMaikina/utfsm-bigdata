from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, from_unixtime, expr, weekofyear, year, to_timestamp, date_format
from pyspark.sql.types import IntegerType
import datetime
import calendar

# Inicializa Spark
spark = SparkSession.builder.getOrCreate()

# Configura bucket
bucket = "204303630-inf356"
input_path = f"s3a://{bucket}/vlt_observations_gc.parquet"
output_base = f"s3a://{bucket}/partition"

# Cargar dataset galáctico
df = spark.read.parquet(input_path)
print(f"Total registros cargados: {df.count()}")

# Convertir 'template_start' de unix timestamp a fecha
df = df.withColumn("ts", to_timestamp((col("template_start").cast("long"))))

# Función auxiliar para calcular "año semántico" y "semana semántica"
def semantic_year_and_week(ts_str):
    dt = datetime.datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    # Buscar primer lunes del año
    jan_1 = datetime.datetime(dt.year, 1, 1)
    first_monday = jan_1 + datetime.timedelta(days=(7 - jan_1.weekday()) % 7)
    if dt < first_monday:
        # Pertenecería al "año anterior"
        year = dt.year - 1
        jan_1_prev = datetime.datetime(year, 1, 1)
        first_monday_prev = jan_1_prev + datetime.timedelta(days=(7 - jan_1_prev.weekday()) % 7)
        week = (dt - first_monday_prev).days // 7
    else:
        year = dt.year
        week = (dt - first_monday).days // 7
    return (year, week)

from pyspark.sql.functions import pandas_udf
import pandas as pd

# Pandas UDF para mejor rendimiento
@pandas_udf("struct<semantic_year:int,semantic_week:int>")
def get_semantic_year_week(ts_series: pd.Series) -> pd.Series:
    result = ts_series.dt.strftime("%Y-%m-%d %H:%M:%S").apply(semantic_year_and_week)
    return pd.DataFrame(result.tolist(), columns=["semantic_year", "semantic_week"])

# Aplicar función
df = df.withColumn("ts_struct", get_semantic_year_week(col("ts")))
df = df.withColumn("semantic_year", col("ts_struct.semantic_year"))
df = df.withColumn("semantic_week", col("ts_struct.semantic_week")).drop("ts_struct")

# Guardar por año
years = df.select("semantic_year").distinct().collect()
for row in years:
    year = row["semantic_year"]
    df_year = df.filter(col("semantic_year") == year)
    
    # Guardar archivo completo del año
    path_year = f"{output_base}/{year}/vlt_observations_{year}.parquet"
    df_year.write.mode("overwrite").parquet(path_year)
    print(f"Año {year} - total registros: {df_year.count()}")

    # Guardar archivos semanales
    weeks = df_year.select("semantic_week").distinct().collect()
    for row_w in weeks:
        week = row_w["semantic_week"]
        df_week = df_year.filter(col("semantic_week") == week)
        path_week = f"{output_base}/{year}/weeks/vlt_observations_{year}_{week:02d}.parquet"
        df_week.write.mode("overwrite").parquet(path_week)
        print(f"    Semana {week:02d} - registros: {df_week.count()}")

# Cerrar sesión Spark
spark.stop()