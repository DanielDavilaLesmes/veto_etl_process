import pandas as pd
from src.config import get_devices_config_data
from src.extract import get_sensor_data
from src.transform import transform_data
from src.load import save_to_sql

def main():
    print("--- INICIANDO VETO ETL (Ubidots -> SQL Server) ---")
    
    # 1. Cargar Configuración
    config = get_devices_config_data()
    if not config: return

    sensores = config.get('sensors', [])
    dispositivos = config.get('devices', [])
    
    print(f"Variables: {len(sensores)} | Dispositivos: {len(dispositivos)}")

    # 2. Bucle por Variable (Estrategia Ubidots)
    for sensor in sensores:
        print(f"\n>>> Procesando Variable Global: {sensor}")
        datos_consolidados_variable = []

        # 3. Extraer de todos los dispositivos
        for device in dispositivos:
            d_label = device.get('device_api_label')
            d_token = device.get('device_token')
            
            if not d_label or not d_token: continue

            # Extracción (Últimos 1000 datos o lógica paginada que tengas)
            raw_data = get_sensor_data(d_label, sensor, d_token)
            
            if raw_data:
                metadata = device.copy()
                metadata['variable_label'] = sensor
                
                # Transformación (Llave_Comun, Hora_10min, etc.)
                df_clean = transform_data(raw_data, metadata)
                
                if not df_clean.empty:
                    datos_consolidados_variable.append(df_clean)
        
        # 4. Inserción Masiva en SQL
        if datos_consolidados_variable:
            df_final = pd.concat(datos_consolidados_variable, ignore_index=True)
            # Insertamos todo el bloque de esta variable en su tabla correspondiente
            save_to_sql(df_final, variable_name=sensor)
        else:
            print(f"   [Info] Sin datos recientes para {sensor}.")

    print("\n--- PROCESO FINALIZADO ---")

if __name__ == "__main__":
    main()