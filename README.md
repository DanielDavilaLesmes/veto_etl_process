
# VETO ETL Process: Ubidots a Excel

Este repositorio contiene una solución **ETL (Extracción, Transformación y Carga)** automatizada diseñada para el proyecto de Excelencia Operacional. Su objetivo es descargar masivamente datos históricos desde la plataforma **Ubidots**, normalizarlos bajo reglas de negocio específicas y generar reportes en Excel agrupados por tipo de variable.

El sistema es **totalmente configurable y portable**, permitiendo gestionar rutas y dispositivos sin modificar el código fuente.

## 📋 Características Técnicas

* **Arquitectura Modular:** Separación clara de responsabilidades en capas (`extract`, `transform`, `load`, `config`).
* **Portabilidad Total:** Uso de rutas absolutas y relativas gestionadas vía `config.json`. Funciona en cualquier entorno (Windows/Linux/Mac) sin cambios de código.
* **Agrupación por Variable:** Genera un único archivo Excel por variable (ej. `tempc_sht.xlsx`) consolidando la data de todos los dispositivos (Pasillos, Sondas, etc.).
* **Normalización Temporal:**
* Conversión automática a Zona Horaria **America/Bogota**.
* Creación de *Buckets* de tiempo de **10 minutos**.
* Generación de `Llave_Comun` (Formato `AAAAMMDDHHMM`) para cruces de datos.


* **Resiliencia:** Manejo de errores de red (SSL/Timeouts) y validación de integridad de datos.

## 📂 Estructura del Proyecto

```text
VETO_ETL_PROCESS/
│
├── config.json                 # ⚙️ Configuración de infraestructura (Rutas y API)
├── config_devices.json         # 📋 Inventario de dispositivos y sensores
├── run_etl.py                  # ▶️ Orquestador principal (Entry Point)
├── requirements.txt            # 📦 Dependencias de Python
├── README.md                   # 📄 Documentación
│
└── src/                        # Código Fuente
    ├── __init__.py
    ├── config.py               # Gestor de rutas y lectura de JSONs
    ├── extract.py              # Cliente HTTP para API Ubidots
    ├── transform.py            # Lógica de negocio y limpieza de datos
    └── load.py                 # Generador de archivos Excel

```

## ⚙️ Configuración del Sistema

El sistema depende de dos archivos JSON que deben estar presentes en la raíz.

### 1. `config.json` (Infraestructura)

Define *dónde* están los archivos y *a dónde* van los resultados. Esto permite migrar el proyecto a otro PC simplemente cambiando estas rutas.

```json
{
  "api": {
    "base_url": "https://industrial.api.ubidots.com/api/v1.6/devices",
    "timeout_seconds": 30
  },
  "rutas": {
    "carpeta_salida": "./Reportes_Finales_2026",  <-- Aquí se guardarán los Excel
    "archivo_dispositivos": "config_devices.json" <-- Nombre del archivo de inventario
  }
}

```

### 2. `config_devices.json` (Negocio)

Define *qué* se va a descargar. Contiene la lista de variables maestras y las credenciales de cada dispositivo.

```json
{
  "sensors": [ "tempc_sht", "bat_status", "humidity" ],
  "devices": [
    {
      "device_name": "P001",
      "device_category": "Pasillo",
      "device_api_label": "eui-a84041f5a186de1a",
      "device_token": "BBUS-XXXXXXXXXXXXXXXXXXXXXXXX"
    },
    ...
  ]
}

```

## 🚀 Instalación y Ejecución

### Prerrequisitos

* Python 3.8 o superior.
* Acceso a internet (Salida HTTPS a `industrial.api.ubidots.com`).

### Pasos

1. **Instalar Dependencias:**
```bash
pip install pandas requests openpyxl

```


*(O usando el archivo requirements: `pip install -r requirements.txt`)*
2. **Verificar Configuración:**
Asegúrese de que `config.json` apunte a las carpetas correctas y que `config_devices.json` tenga los tokens actualizados.
3. **Ejecutar el ETL:**
```bash
python run_etl.py

```



## 📊 Salida de Datos (Output)

Al finalizar la ejecución, el sistema creará automáticamente la carpeta definida en `config.json` (ej: `Reportes_Finales_2026`).

Dentro encontrará un archivo `.xlsx` por cada sensor definido en la lista `sensors`.

**Ejemplo: `tempc_sht.xlsx**`
Este archivo contendrá todas las lecturas de temperatura de *todos* los pasillos y sondas, con la siguiente estructura tabular:

| Llave_Comun | Pasillo | Pasillo_est | Anio | Mes | Dia | Hora_10min | FechaHora_Original | Variable | Valor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **202601271450** | Pasillo 1 | P001 | 2026 | 01 | 27 | **14:50** | 27/01/2026 14:53:12 | tempc_sht | -18.5 |
| **202601271450** | Sonda 4 | S004 | 2026 | 01 | 27 | **14:50** | 27/01/2026 14:51:00 | tempc_sht | -20.1 |

* **Llave_Comun:** Identificador único temporal para cruces (AñoMesDiaHoraMinuto).
* **Hora_10min:** Hora redondeada al múltiplo inferior de 10 minutos (Regla de negocio).

## ⚠️ Solución de Problemas Comunes

1. **"Config Warning: config.json no encontrado"**
* El script utiliza detección de rutas absolutas. Asegúrese de que `config.json` esté en la misma carpeta que `run_etl.py`, no dentro de `src/`.


2. **Errores SSL / Timeouts**
* El código tiene desactivada la verificación SSL (`verify=False`) para compatibilidad con redes corporativas estrictas. Si persiste, revise la conexión a internet.


3. **Datos Vacíos**
* Si un archivo Excel se genera vacío o no se genera, verifique que el `device_api_label` en el JSON coincida exactamente con el de la plataforma Ubidots.



---

**Desarrollador:** Equipo de Desarrollo / Daniel Davila - OPEX IceStar
**Última Actualización:** Enero 2026