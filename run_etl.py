import pandas as pd
from src.config import load_config
from src.extract import get_sensor_data
from src.transform import transform_data
from src.load import save_sensor_file

def main():
    print("--- INICIANDO ETL: AGRUPADO POR VARIABLE ---")
    config = load_config()
    if not config: return

    sensores = config['sensors']      # Lista de variables (tempc_sht, bat_status, etc.)
    dispositivos = config['devices']  # Lista de los 43 dispositivos
    
    print(f"Total Variables: {len(sensores)}")
    print(f"Total Dispositivos: {len(dispositivos)}")

    # 1. BUCLE EXTERNO: Por Variable (Para generar un archivo por variable)
    for sensor in sensores:
        print(f"\n>>> Procesando Variable Global: {sensor}")
        datos_consolidados_variable = []

        # 2. BUCLE INTERNO: Buscar esa variable en TODOS los dispositivos
        for device in dispositivos:
            d_name = device.get('device_name', 'S_N')
            d_label = device.get('device_api_label')
            d_token = device.get('device_token')
            
            # Validación simple
            if not d_label or not d_token: continue

            # print(f"   Consulta: {d_name}...", end="\r") # Opcional: para ver progreso

            # A. Extracción (Últimos 1000 datos)
            raw_data = get_sensor_data(d_label, sensor, d_token)
            
            if raw_data:
                # Preparamos metadatos
                metadata = device.copy()
                metadata['variable_label'] = sensor
                
                # B. Transformación (Genera Llave_Comun, Hora_10min, etc.)
                df_clean = transform_data(raw_data, metadata)
                
                if not df_clean.empty:
                    datos_consolidados_variable.append(df_clean)
        
        # 3. CARGA: Guardar archivo único para la variable actual
        if datos_consolidados_variable:
            df_final = pd.concat(datos_consolidados_variable, ignore_index=True)
            save_sensor_file(df_final, sensor_name=sensor)
            print(f"   [OK] {sensor}.xlsx generado con {len(df_final)} registros totales.")
        else:
            print(f"   [Vacío] No se encontraron datos para {sensor} en ningún dispositivo.")

    print("\n--- PROCESO FINALIZADO ---")

if __name__ == "__main__":
    main()