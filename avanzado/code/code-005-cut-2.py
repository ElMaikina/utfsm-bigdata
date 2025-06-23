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