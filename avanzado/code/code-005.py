from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col, split

# Bucket personal (reemplaza con tu RUT sin puntos ni guion)
bucket = "204303630-inf356"

# Iniciar sesión Spark
spark = SparkSession.builder.getOrCreate()

# Esquema de datos
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

# Leer y unir los 20 archivos
df_list = []
for i in range(20):
    filename = f"vlt_observations_{i:03}.csv"
    path = f"s3a://utfsm-inf356-datasets/vlt_observations/{filename}"
    print(f"Loading: {filename}")
    df = spark.read.csv(path, header=False, schema=schema)
    df_list.append(df)

df_all = df_list[0]
for df in df_list[1:]:
    df_all = df_all.union(df)

# Filtrar solo observaciones válidas
df_filtered = df_all.filter((col("category") == "SCIENCE") & (col("obs_type") == "OBJECT"))

# Separar coordenadas RA y DEC
df_split = df_filtered \
    .withColumn("ra_deg", split(col("right_ascension"), " ").getItem(0)) \
    .withColumn("ra_min", split(col("right_ascension"), " ").getItem(1)) \
    .withColumn("ra_sec", split(col("right_ascension"), " ").getItem(2)) \
    .withColumn("dec_deg", split(col("declination"), " ").getItem(0)) \
    .withColumn("dec_min", split(col("declination"), " ").getItem(1)) \
    .withColumn("dec_sec", split(col("declination"), " ").getItem(2)) \
    .withColumn("template_start_unix", col("template_start").cast("long")) \
    .withColumn("exposition_time", col("exposition_time").cast("float"))

# Seleccionar columnas finales
df_final = df_split.select(
    "ra_deg", "ra_min", "ra_sec",
    "dec_deg", "dec_min", "dec_sec",
    "instrument", "exposition_time", "template_start_unix"
)

# Guardar como Parquet
output_path = f"s3a://{bucket}/vlt_observations_etl.parquet"
print(f"Saving processed data to {output_path}")
df_final.write.mode("overwrite").parquet(output_path)

# Métrica: filas procesadas
print(f"Filas finales procesadas: {df_final.count()}")

# Terminar sesión
spark.stop()