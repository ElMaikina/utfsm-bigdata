from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType
from pyspark.sql.functions import col, split, udf

# Bucket personal
bucket = "204303630-inf356"

# Direccion de salida
output_path = f"s3a://{bucket}/vlt_observations_etl.parquet"

# Iniciar Spark
spark = SparkSession.builder.getOrCreate()

# Formato de los datos
schema = StructType([
    StructField("object", StringType(), True),
    StructField("right_ascension", StringType(), True),
    StructField("declination", StringType(), True),
    StructField("obs_timestamp", StringType(), True),
    StructField("program_id", StringType(), True),
    StructField("investigators", StringType(), True),
    StructField("obs_mode", StringType(), True),
    StructField("title", StringType(), True),
    StructField("program_type", StringType(), True),
    StructField("instrument", StringType(), True),
    StructField("category", StringType(), True),
    StructField("obs_type", StringType(), True),
    StructField("obs_nature", StringType(), True),
    StructField("dataset_id", StringType(), True),
    StructField("obs_file", StringType(), True),
    StructField("release_date", StringType(), True),
    StructField("obs_name", StringType(), True),
    StructField("obs_id", StringType(), True),
    StructField("template_id", StringType(), True),
    StructField("template_start", StringType(), True),
    StructField("exposition_time", StringType(), True),
    StructField("filter_lambda_min", StringType(), True),
    StructField("filter_lambda_max", StringType(), True),
    StructField("filter", StringType(), True),
    StructField("grism", StringType(), True),
    StructField("grating", StringType(), True),
    StructField("slit", StringType(), True),
    StructField("obs_mjd", StringType(), True),
    StructField("airmass", StringType(), True),
    StructField("seeing", StringType(), True),
    StructField("distance", StringType(), True),
    StructField("position", StringType(), True)
])

# Lee y une los segmentos del archivo original
df_list = []
for i in range(20):
    filename = f"vlt_observations_{i:03}.csv"
    path = f"s3a://utfsm-inf356-datasets/vlt_observations/{filename}"
    print(f"Trying to load data segment '{filename}'...")
    df = spark.read.csv(path, header=False, schema=schema)
    print(f"Succesfully loaded data segment '{filename}'!")
    df_list.append(df)

df_all = df_list[0]
for df in df_list[1:]:
    df_all = df_all.union(df)

# Muestra los datos iniciales
df_all.show(n=20)

# Borra todas las filas con valores nulos
df_all.na.drop()

# Filtra en base a la categoria solicitada
df_filtered = df_all.filter((col("category") == "SCIENCE") & (col("obs_type") == "OBJECT"))

# Separar coordenadas right ascension y declination
df_split = df_filtered \
    .withColumn("ra_deg", split(col("right_ascension"), ":").getItem(0)) \
    .withColumn("ra_min", split(col("right_ascension"), ":").getItem(1)) \
    .withColumn("ra_sec", split(col("right_ascension"), ":").getItem(2)) \
    .withColumn("dec_deg", split(col("declination"), ":").getItem(0)) \
    .withColumn("dec_min", split(col("declination"), ":").getItem(1)) \
    .withColumn("dec_sec", split(col("declination"), ":").getItem(2)) \
    .withColumn("date", split(col("template_start"), "T").getItem(0)) \
    .withColumn("time", split(col("template_start"), "T").getItem(1)) \
    .withColumn("exposition_time", col("exposition_time").cast("float"))

# Separa las fechas en meses, dias, horas, etc.
df_split = df_split \
    .withColumn("year", split(col("date"), "-").getItem(0).cast("long")) \
    .withColumn("month", split(col("date"), "-").getItem(1).cast("long")) \
    .withColumn("day", split(col("date"), "-").getItem(2).cast("long")) \
    .withColumn("hours", split(col("time"), ":").getItem(0).cast("long")) \
    .withColumn("minutes", split(col("time"), ":").getItem(1).cast("long")) \
    .withColumn("seconds", split(col("time"), ":").getItem(2).cast("long")) \

# Funcion lambda que determina si un ano es bisiesto
leap = lambda y: int((y % 4 == 0 and y % 100 != 0) or (y % 400 == 0))

# Funcion lambda que devuelve la cantidad de dias de cada mes
days_per_month = lambda y: [0, 31, 28 + int(leap(y)), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Calcula la cantidad de anos bisiestos desde 1970 hasta el ano indicado
sum_leap_years = lambda y: int(sum([i for i in range(1970, y) if leap(i) == 1]))

# Suma los dias totales de cada ano desde 1970 hasta el ano indicado
sum_days_in_years = lambda y: int(365 * (y - 1970) + sum_leap_years(y))

# Suma los dias totales de cada mes desde enero hasta el mes indicado
sum_days_in_months = lambda m: int(sum([i for i in range(0, m+1) if days_per_month(i) != 0]))

# Obtiene los dias totales desde 1970 hasta la fecha actual
sum_total_days = lambda y, m, d: int(sum_days_in_years(y) + sum_days_in_months(m) + d)

# Funcion que obtiene el tiempo en formato unix de forma manual
manual_unix_time =  lambda Y, M, D, h, m, s: int(sum_total_days(Y,M,D) * 86400 + h * 3600 + m * 60 + s)

# Funcion que puede aplicarse a las columnas de el dataframe de PySpark
df_manual_unix_time = udf(manual_unix_time,LongType())

# Finalmente aplica la funcion para obtener el tiempo en formato unix
df_split = df_split.withColumn("template_start_unix", df_manual_unix_time(col("year"), col("month"), col("day"), col("hours"), col("minutes"), col("seconds")))

# Selecciona solo las columnas utiles
df_final = df_split.select(
    "ra_deg", "ra_min", "ra_sec",
    "dec_deg", "dec_min", "dec_sec",
    "instrument", "exposition_time", "template_start_unix"
)

# Guarda el dataframe como parquet
print(f"Attempting to save processed data to '{output_path}'...")
df_final.write.mode("overwrite").parquet(output_path)
print(f"Succesfully saved processed data to '{output_path}'!")

# Muestra las filas procesadas
print(f"Final processed rows: {df_final}")
print(f"Final rows extracted: {df_final.count()}")
print(f"Final processed data:")
df_final.show(n=20)

# Detiene Spark
spark.stop()