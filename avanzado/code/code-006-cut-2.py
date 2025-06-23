# Calcula las coordenadas galacticas
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
# Devuelve las coordenadas a esfericas
df = df.withColumn("gal_ra", (degrees(atan2(col("y_gal"), col("x_gal"))) + 360) % 360)
df = df.withColumn("gal_dec", degrees(asin(col("z_gal"))))
# Toma sola las columnas deseadas
df_final = df.select(
    col("gal_ra"),
    col("gal_dec"),
    col("instrument"),
    col("exposition_time"),
    col("template_start_unix")
)
# Guarda el dataframe como parquet
df_final.write.mode("overwrite").parquet(output_path)
# Muestra las filas procesadas
print(f"Final processed rows: {df_final}")
print(f"Final rows extracted: {df_final.count()}")
print(f"Final processed data:")
df_final.show(n=20)
# Detiene Spark
spark.stop()