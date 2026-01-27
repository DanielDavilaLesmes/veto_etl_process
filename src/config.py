import json
import os

# Constantes Globales
BASE_URL = "https://industrial.api.ubidots.com/api/v1.6/devices"
CONFIG_FILE = 'config_devices.json'

def load_config(file_path=CONFIG_FILE):
    """
    Carga y valida el archivo de configuración JSON.
    Retorna el diccionario completo o None si hay error.
    """
    if not os.path.exists(file_path):
        print(f"[Config] Error: No se encontró el archivo {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Validación simple de estructura
            if 'sensors' not in data or 'devices' not in data:
                print("[Config] Error: El JSON debe contener 'sensors' y 'devices'.")
                return None
            return data
    except Exception as e:
        print(f"[Config] Error leyendo configuración: {e}")
        return None