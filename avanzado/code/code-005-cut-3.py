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