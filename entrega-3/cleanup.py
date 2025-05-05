import csv
import re

# Lee el archivo original y guarda la correccion en otro archivo
with open("vlt_observations_000.csv") as fin, open("vlt_observations_000_clean.csv", "w") as fout:
    for line in fin:
        # Reemplaza comas dentro de paréntesis por otro carácter temporal
        line_fixed = re.sub(r'\(([^()]*)\)', lambda m: m.group(0).replace(",", " "), line)
        # Muestra por pantalla la linea a corregir
        print(f"Linea a corregir: {line_fixed}")
        # Escribe en el archivo la linea corregida
        fout.write(line_fixed)