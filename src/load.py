import pandas as pd
import os
from src.config import get_output_path

def save_sensor_file(df, sensor_name):
    if df.empty: return

    # 1. Obtenemos la ruta desde el JSON
    output_folder = get_output_path()
    
    # 2. Aseguramos que la carpeta exista
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except OSError as e:
            print(f"      [Error] No se pudo crear carpeta {output_folder}: {e}")
            return

    # 3. Guardado
    safe_name = str(sensor_name).replace(" ", "_").replace("/", "-")
    filename = os.path.join(output_folder, f"{safe_name}.xlsx")
    
    try:
        df.to_excel(filename, index=False)
    except Exception as e:
        print(f"      [Error IO] Fallo al escribir {filename}: {e}")