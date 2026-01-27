import pandas as pd
import os

# IMPORTS ACTUALIZADOS: Usamos los nuevos getters
from src.config import get_devices_config_data, get_output_path 
from src.extract import get_sensor_data
from src.transform import transform_data
from src.load import save_sensor_file

def main():
    print("--- INICIANDO ETL (Versión Configuración Externa) ---")
    
    # 1. Cargar configuración de dispositivos
    config = get_devices_config_data()
    
    if not config:
        print("Deteniendo ejecución: No se pudo cargar la configuración de dispositivos.")
        return

    # Extraer listas del JSON
    sensores = config.get('sensors', [])
    dispositivos = config.get('devices', [])
    ruta_salida = get_output_path()
    
    print(f"Ruta de Salida: {ruta_salida}")
    print(f"Variables a procesar: {len(sensores)}")
    print(f"Dispositivos configurados: {len(dispositivos)}")

    # 2. Iterar por cada Variable (Sensor)
    for sensor in sensores:
        print(f"\n>>> Procesando Variable: {sensor}")
        datos_consolidados_variable = []

        # 3. Buscar esta variable en TODOS los dispositivos
        for device in dispositivos:
            d_name = device.get('device_name', 'S_N')
            d_label = device.get('device_api_label')
            d_token = device.get('device_token')
            
            # Validación de seguridad
            if not d_label or not d_token: 
                continue

            # A. Extracción
            raw_data = get_sensor_data(d_label, sensor, d_token)
            
            if raw_data:
                # Preparamos metadatos para la transformación
                metadata = device.copy()
                metadata['variable_label'] = sensor
                
                # B. Transformación
                df_clean = transform_data(raw_data, metadata)
                
                if not df_clean.empty:
                    datos_consolidados_variable.append(df_clean)
        
        # 4. Guardado (Carga)
        if datos_consolidados_variable:
            df_final = pd.concat(datos_consolidados_variable, ignore_index=True)
            save_sensor_file(df_final, sensor_name=sensor)
            print(f"   [OK] Archivo generado con {len(df_final)} registros.")
        else:
            print(f"   [Info] No se encontraron datos para {sensor}.")

    print("\n--- PROCESO FINALIZADO ---")

if __name__ == "__main__":
    main()