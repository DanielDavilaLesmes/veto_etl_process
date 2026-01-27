import requests
import urllib3
from src.config import get_base_url 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_sensor_data(device_label, variable_label, token):
    # CAMBIO: Obtenemos la URL dinámicamente
    base_url = get_base_url()
    
    # Construcción de la ruta
    url = f"{base_url}/{device_label}/{variable_label}/values"
    
    params = {
        "token": token,
        "page_size": 1000 
    }
    
    try:
        response = requests.get(url, params=params, verify=False)
        
        if response.status_code == 404:
            return []
        
        if response.status_code == 403:
            print(f"   [!] Error 403 (Permisos) en {variable_label}")
            return []

        response.raise_for_status()
        data = response.json()
        
        if 'results' in data and data['results']:
            return data['results']
        
        return []

    except Exception as e:
        print(f"   [Error API] {variable_label}: {e}")
        return []