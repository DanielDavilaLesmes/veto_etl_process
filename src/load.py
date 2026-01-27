import pandas as pd
import os

# Crear carpeta de salida si no existe
OUTPUT_FOLDER = "Resultados_Por_Variable"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def save_sensor_file(df, sensor_name):
    """
    Guarda el acumulado de TODOS los dispositivos para una variable específica.
    Nombre del archivo: NombreVariable.xlsx (ej: tempc_sht.xlsx)
    """
    if df.empty:
        return

    # Limpieza de nombre de archivo
    safe_name = str(sensor_name).replace(" ", "_").replace("/", "-")
    filename = f"{OUTPUT_FOLDER}/{safe_name}.xlsx"
    
    try:
        # Guardamos sin index
        df.to_excel(filename, index=False)
    except Exception as e:
        print(f"      [Error Guardando] {filename}: {e}")