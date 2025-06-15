from pyspark.sql import SparkSession
from pyspark.sql.functions import col, radians, degrees, cos, sin, atan2, asin

# Create SparkSession
spark = SparkSession.builder.getOrCreate()

# Load parquet from previous ETL step
bucket = "204303630-inf356"
input_path = f"s3a://{bucket}/vlt_observations_etl.parquet"
df = spark.read.parquet(input_path)

# Convert RA/DEC from HMS/DMS to decimal degrees (float) if needed
# Here we assume those columns are already floats in decimal degrees.

# Convert to radians for trigonometric functions
df = df.withColumn("ra_rad", radians(
    col("Right ascension - grados") +
    col("Right ascension - minutos") / 60 +
    col("Right ascension - segundos") / 3600
)).withColumn("dec_rad", radians(
    col("Declination - grados") +
    col("Declination - minutos") / 60 +
    col("Declination - segundos") / 3600
))

# Compute Cartesian coordinates
df = df.withColumn("x_eq", cos(col("dec_rad")) * cos(col("ra_rad")))
df = df.withColumn("y_eq", cos(col("dec_rad")) * sin(col("ra_rad")))
df = df.withColumn("z_eq", sin(col("dec_rad")))

# Apply rotation matrix from Equatorial (J2000) to Galactic coordinates
df = df.withColumn("x_gal", 
    -0.05487556 * col("x_eq") +
    -0.87343709 * col("y_eq") +
    -0.48383502 * col("z_eq")
).withColumn("y_gal", 
     0.49410943 * col("x_eq") +
    -0.44482963 * col("y_eq") +
     0.74698225 * col("z_eq")
).withColumn("z_gal", 
    -0.86766615 * col("x_eq") +
    -0.19807637 * col("y_eq") +
     0.45598378 * col("z_eq")
)

# Convert back to spherical galactic coordinates (in degrees)
df = df.withColumn("gal_l", (degrees(atan2(col("y_gal"), col("x_gal"))) + 360) % 360)
df = df.withColumn("gal_b", degrees(asin(col("z_gal"))))

# Select required columns
df_final = df.select(
    col("gal_l").alias("Galactic right ascension"),
    col("gal_b").alias("Galactic declination"),
    col("Instrument"),
    col("Exposition time"),
    col("Template start")
)

# Save result as Parquet
output_path = f"s3a://{bucket}/vlt_observations_gc.parquet"
df_final.write.mode("overwrite").parquet(output_path)

# Stop Spark session
spark.stop()