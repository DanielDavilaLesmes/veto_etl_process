import json
import os

# --- GESTIÓN DE RUTAS ABSOLUTAS ---
# Detectamos la ruta de este archivo (src/config.py) y subimos un nivel para hallar la raíz
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

# Ruta absoluta al config.json
APP_CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config.json')

# Caché de configuración con valores por defecto
CONFIG_CACHE = {
    "base_url": "https://industrial.api.ubidots.com/api/v1.6/devices",
    "output_dir": os.path.join(PROJECT_ROOT, "Resultados"),
    "device_config": os.path.join(PROJECT_ROOT, "config_devices.json")
}

def load_settings():
    """
    Carga config.json usando rutas absolutas.
    """
    global CONFIG_CACHE
    
    if not os.path.exists(APP_CONFIG_FILE):
        print(f"[Config] Advertencia: No se encontró {APP_CONFIG_FILE}")
        print(f"         Buscando en: {APP_CONFIG_FILE}")
        print("         Usando valores por defecto.")
        return

    try:
        with open(APP_CONFIG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 1. API URL
            if 'api' in data:
                CONFIG_CACHE['base_url'] = data['api'].get('base_url', CONFIG_CACHE['base_url'])
            
            # 2. Rutas (Convertimos relativas a absolutas si es necesario)
            if 'rutas' in data:
                raw_out = data['rutas'].get('carpeta_salida', 'Resultados')
                raw_dev = data['rutas'].get('archivo_dispositivos', 'config_devices.json')
                
                # Si las rutas en el JSON empiezan con "./", las unimos al ROOT
                if raw_out.startswith("./") or raw_out.startswith(".\\"):
                    CONFIG_CACHE['output_dir'] = os.path.join(PROJECT_ROOT, raw_out[2:])
                else:
                    CONFIG_CACHE['output_dir'] = raw_out

                if raw_dev.startswith("./") or raw_dev.startswith(".\\"):
                    CONFIG_CACHE['device_config'] = os.path.join(PROJECT_ROOT, raw_dev[2:])
                else:
                    CONFIG_CACHE['device_config'] = raw_dev
                    
    except Exception as e:
        print(f"[Config] Error crítico leyendo config.json: {e}")

# Carga inicial automática
load_settings()

# --- GETTERS (Funciones públicas) ---

def get_base_url():
    return CONFIG_CACHE['base_url']

def get_output_path():
    return CONFIG_CACHE['output_dir']

def get_devices_config_data():
    """
    Lee y retorna el JSON de dispositivos.
    """
    path = CONFIG_CACHE['device_config']
    
    if not os.path.exists(path):
        print(f"[Config] Error: No existe el archivo de dispositivos en: {path}")
        return None
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Config] Error procesando {path}: {e}")
        return None