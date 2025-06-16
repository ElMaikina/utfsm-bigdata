from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, unix_timestamp, regexp_replace
from pyspark.sql.types import StructType, StructField, StringType

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
print(f"Initial unprocessed rows:")
df_all.show(n=20)

# Borra todas las filas con valores nulos
df_all.na.drop(how='any')

# Toma una muestra de los anos para acelerar el proceso
df_all = df_all.sample(fraction=0.25, seed=3)

# Quita las filas con valores nulos
df_all = df_all.where(col("template_start").isNotNull())

# Filtra en base a la categoria solicitada
df_filtered = df_all.filter((col("category") == "SCIENCE") & (col("obs_type") == "OBJECT"))

# Arregla el formato del time stamp que usa el dataframe original
df_filtered = df_filtered.withColumn("template_start", regexp_replace("template_start", r"T", " "))

# Separar coordenadas right ascension y declination
df_split = df_filtered \
    .withColumn("ra_deg", split(col("right_ascension"), ":").getItem(0)) \
    .withColumn("ra_min", split(col("right_ascension"), ":").getItem(1)) \
    .withColumn("ra_sec", split(col("right_ascension"), ":").getItem(2)) \
    .withColumn("dec_deg", split(col("declination"), ":").getItem(0)) \
    .withColumn("dec_min", split(col("declination"), ":").getItem(1)) \
    .withColumn("dec_sec", split(col("declination"), ":").getItem(2)) \
    .withColumn("template_start_unix", unix_timestamp("template_start")) \
    .withColumn("exposition_time", col("exposition_time").cast("float"))

# Selecciona solo las columnas utiles
df_final = df_split.select(
    "ra_deg", "ra_min", "ra_sec",
    "dec_deg", "dec_min", "dec_sec",
    "instrument", "exposition_time", 
    "template_start_unix"
)

# Elimina los registros sin fecha
df_final = df_final.where(col("template_start_unix").isNotNull())

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