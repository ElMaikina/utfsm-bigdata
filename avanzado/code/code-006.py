from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import FloatType
from astropy.coordinates import SkyCoord
import astropy.units as u

# Iniciar Spark
spark = SparkSession.builder.getOrCreate()

# Reemplaza con tu número de estudiante sin puntos ni guión
bucket = "204303630-inf356"
input_path = f"s3a://{bucket}/vlt_observations_etl.parquet"
output_path = f"s3a://{bucket}/vlt_observations_gc.parquet"

# Leer dataset procesado
df = spark.read.parquet(input_path)
print(f"Filas leídas: {df.count()}")

# UDF para convertir coordenadas ecuatoriales a galácticas
def equatorial_to_galactic(ra_deg, ra_min, ra_sec, dec_deg, dec_min, dec_sec):
    try:
        # Convertir a float
        ra = float(ra_deg) + float(ra_min) / 60 + float(ra_sec) / 3600
        dec_sign = -1 if str(dec_deg).strip().startswith('-') else 1
        dec = abs(float(dec_deg)) + float(dec_min) / 60 + float(dec_sec) / 3600
        dec *= dec_sign
        coord = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
        return float(coord.galactic.l.degree), float(coord.galactic.b.degree)
    except:
        return None

# Registrar UDF para coordenadas galácticas separadas
@udf(FloatType())
def ra_galactic_udf(ra_deg, ra_min, ra_sec, dec_deg, dec_min, dec_sec):
    result = equatorial_to_galactic(ra_deg, ra_min, ra_sec, dec_deg, dec_min, dec_sec)
    return result[0] if result else None

@udf(FloatType())
def dec_galactic_udf(ra_deg, ra_min, ra_sec, dec_deg, dec_min, dec_sec):
    result = equatorial_to_galactic(ra_deg, ra_min, ra_sec, dec_deg, dec_min, dec_sec)
    return result[1] if result else None

# Aplicar UDFs al DataFrame
df_gc = df.withColumn("ra_galactic", ra_galactic_udf(
        col("ra_deg"), col("ra_min"), col("ra_sec"),
        col("dec_deg"), col("dec_min"), col("dec_sec")
    )) \
    .withColumn("dec_galactic", dec_galactic_udf(
        col("ra_deg"), col("ra_min"), col("ra_sec"),
        col("dec_deg"), col("dec_min"), col("dec_sec")
    ))

# Seleccionar columnas requeridas
df_final = df_gc.select(
    "ra_galactic",
    "dec_galactic",
    "instrument",
    "exposition_time",
    "template_start_unix"
)

# Eliminar filas con coordenadas inválidas
df_final = df_final.na.drop()

# Guardar resultado
df_final.write.mode("overwrite").parquet(output_path)

print(f"Archivo generado: {output_path}")
print(f"Filas transformadas y guardadas: {df_final.count()}")

# Cerrar Spark
spark.stop()