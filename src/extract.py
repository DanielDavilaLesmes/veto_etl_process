import requests
import urllib3
from src.config import BASE_URL

# Desactivar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_sensor_data(device_label, variable_label, token):
    """
    Descarga los últimos XX datos.
    """
    url = f"{BASE_URL}/{device_label}/{variable_label}/values"
    
    params = {
        "token": token,
        "page_size": 100000  # Ajustable según necesidad
    }
    
    try:
        # verify=False para evitar bloqueo de certificado
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