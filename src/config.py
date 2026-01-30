import json
import os

# Rutas dinámicas
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
APP_CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config.json')

CONFIG_CACHE = {}

def load_settings():
    global CONFIG_CACHE
    if not os.path.exists(APP_CONFIG_FILE):
        print(f"[Config] Error: No se encontró {APP_CONFIG_FILE}")
        return

    try:
        with open(APP_CONFIG_FILE, 'r', encoding='utf-8') as f:
            CONFIG_CACHE = json.load(f)
            
            # Ajuste de rutas relativas
            if 'rutas' in CONFIG_CACHE:
                raw_dev = CONFIG_CACHE['rutas'].get('archivo_dispositivos', 'config_devices.json')
                if raw_dev.startswith("./") or raw_dev.startswith(".\\"):
                    CONFIG_CACHE['rutas']['archivo_dispositivos'] = os.path.join(PROJECT_ROOT, raw_dev[2:])
                else:
                    CONFIG_CACHE['rutas']['archivo_dispositivos'] = raw_dev
                    
    except Exception as e:
        print(f"[Config] Error leyendo JSON: {e}")

load_settings()

# --- GETTERS ---

def get_base_url():
    return CONFIG_CACHE.get('api', {}).get('base_url')

def get_db_config():
    """Retorna la configuración de base de datos"""
    return CONFIG_CACHE.get('database', {})

def get_devices_config_data():
    path = CONFIG_CACHE.get('rutas', {}).get('archivo_dispositivos')
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None