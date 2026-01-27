import pandas as pd

def round_to_10min(dt):
    """
    Recibe un objeto datetime y redondea los minutos al múltiplo de 10 inferior.
    Ej: 13:58 -> 13:50, 13:02 -> 13:00
    """
    minute = (dt.minute // 10) * 10
    return dt.replace(minute=minute, second=0, microsecond=0)

def transform_data(raw_data, metadata):
    if not raw_data:
        return pd.DataFrame()

    df = pd.DataFrame(raw_data)

    # 1. Limpieza básica
    if 'value' in df.columns and 'timestamp' in df.columns:
        df = df[['value', 'timestamp']].copy()
        df.columns = ['Valor', 'Timestamp_Unix']
        
        # 2. Conversión temporal (Zona Horaria Colombia)
        df['FechaHora_Original'] = pd.to_datetime(df['Timestamp_Unix'], unit='ms')
        df['FechaHora_Original'] = df['FechaHora_Original'].dt.tz_localize('UTC').dt.tz_convert('America/Bogota')
        
        # --- LÓGICA DE AGRUPACIÓN (10 MINUTOS) ---
        
        # Creamos una columna temporal con la fecha redondeada a 10 min
        # Usamos apply para procesar fila por fila o vectorizado
        fecha_redondeada = df['FechaHora_Original'].apply(round_to_10min)
        
        # 3. Creación de Campos Estructurales (Según su imagen)
        
        # Desglose de Fecha
        df['Anio'] = fecha_redondeada.dt.year
        df['Mes'] = fecha_redondeada.dt.month
        df['Dia'] = fecha_redondeada.dt.day
        
        # Hora cerrada (Ej: 00:10, 13:50)
        df['Hora_10min'] = fecha_redondeada.dt.strftime('%H:%M')
        
        # Llave Común: Formato AAAAMMDDHHMM (usando los minutos redondeados)
        # Convertimos a string y eliminamos caracteres no numéricos
        df['Llave_Comun'] = fecha_redondeada.dt.strftime('%Y%m%d%H%M')
        
        # 4. Metadatos del Dispositivo
        df['Pasillo'] = metadata.get('device_category')        # Ej: Pasillo 1
        df['Pasillo_est'] = metadata.get('device_name')    # O device_ID si prefiere
        df['Variable'] = metadata.get('variable_label')
        
        # Limpieza para Excel (quitamos zona horaria de la original para que Excel no falle)
        df['FechaHora_Original'] = df['FechaHora_Original'].dt.tz_localize(None)
        
        # Selección final de columnas en el orden deseado
        cols = [
            'Llave_Comun', 
            'Pasillo', 
            'Pasillo_est', 
            'Anio', 
            'Mes', 
            'Dia', 
            'Hora_10min', 
            'FechaHora_Original', 
            'Variable', 
            'Valor'
        ]
        
        return df[cols]
    
    return pd.DataFrame()