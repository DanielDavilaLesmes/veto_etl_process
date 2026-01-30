
# VETO ETL Process: Ubidots a SQL Server

Este repositorio contiene la solución de ingeniería de datos para el proyecto de Excelencia Operacional. Automatiza la extracción masiva de datos desde la nube de **Ubidots**, aplica normalización temporal y reglas de negocio, y carga los resultados directamente en una base de datos **SQL Server** corporativa.

El sistema está diseñado para ser **modular, portable y altamente configurable**.

## 📋 Características Técnicas

* **Integración Directa a SQL:** Reemplaza los archivos planos por inserción directa en base de datos usando `SQLAlchemy` (ORM) y `Fast Executemany` para alto rendimiento.
* **Normalización Temporal:**
* Conversión de *Unix Timestamps* a Zona Horaria **America/Bogota**.
* Generación de *Buckets* de tiempo de **10 minutos** para estandarizar cruces de información.
* Creación de llave primaria compuesta (`Llave_Comun`: `AAAAMMDDHHMM`).


* **Arquitectura Configurable:** Gestión de credenciales, rutas y parámetros de negocio separados del código fuente (`config.json` y `config_devices.json`).
* **Gestión Dinámica de Tablas:** Crea o actualiza tablas automáticamente basándose en el nombre de la variable (ej. `tempc_sht` -> `ind_Veto_tempc_sht`).

## 📂 Estructura del Proyecto

```text
VETO_ETL_PROCESS/
│
├── config.json                 # ⚙️ Infraestructura: Credenciales DB y API
├── config_devices.json         # 📋 Negocio: Inventario de dispositivos y variables
├── run_etl.py                  # ▶️ Orquestador principal
├── requirements.txt            # 📦 Librerías necesarias
├── README.md                   # 📄 Documentación
│
└── src/                        # Código Fuente
    ├── __init__.py
    ├── config.py               # Lector de configuraciones
    ├── extract.py              # Cliente API Ubidots
    ├── transform.py            # Lógica de limpieza y fechas
    └── load.py                 # Conector SQL Server (Insert)

```

## ⚙️ Requisitos Previos

1. **Python 3.8+** instalado.
2. **ODBC Driver 17 for SQL Server**: Necesario para que Python (`pyodbc`) se comunique con SQL Server. [Descargar aquí](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).
3. Acceso de red a:
* `industrial.api.ubidots.com` (HTTPS/443).
* Servidor SQL Corporativo (Puerto estándar 1433).



## 🔧 Configuración

El sistema depende de dos archivos JSON en la raíz:

### 1. `config.json` (Infraestructura)

Define las credenciales de la base de datos y la API. **No compartir este archivo públicamente.**

```json
{
  "api": {
    "base_url": "https://industrial.api.ubidots.com/api/v1.6/devices",
    "timeout_seconds": 30
  },
  "database": {
    "server": "192.168.X.X",
    "database": "Indicadores",
    "username": "sa",
    "password": "StrongPassword!",
    "driver": "ODBC Driver 17 for SQL Server",
    "table_prefix": "ind_Veto_"   <-- Prefijo para las tablas creadas
  },
  "rutas": {
    "archivo_dispositivos": "config_devices.json"
  }
}

```

### 2. `config_devices.json` (Negocio)

Define qué variables buscar y en qué dispositivos.

```json
{
  "sensors": [ "tempc_sht", "bat_status" ],
  "devices": [
    {
      "device_name": "P001",
      "device_category": "Pasillos",
      "device_api_label": "eui-xxxxxxxxxxxx",
      "device_token": "BBUS-xxxxxxxxxxxx"
    }
  ]
}

```

## 🚀 Instalación y Ejecución

1. **Crear entorno virtual (Recomendado):**
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows

```


2. **Instalar dependencias:**
```bash
pip install -r requirements.txt

```


3. **Ejecutar el proceso:**
```bash
python run_etl.py

```



## 📊 Modelo de Datos (Output en SQL)

El sistema insertará los datos en la base de datos definida. El nombre de la tabla se genera dinámicamente:
`[table_prefix] + [nombre_variable]`

**Ejemplo:** Para la variable `tempc_sht`, la tabla será `dbo.ind_Veto_tempc_sht`.

**Estructura de la tabla:**

| Columna | Tipo | Descripción |
| --- | --- | --- |
| **Llave_Comun** | `nvarchar` | ID Temporal (AAAAMMDDHHMM). |
| **Pasillo** | `nvarchar` | Nombre descriptivo del dispositivo (ej. Pasillo 1). |
| **Pasillo_est** | `nvarchar` | Nombre técnico o corto (ej. P001). |
| **Anio** | `int` | Año de la medición. |
| **Mes** | `int` | Mes de la medición. |
| **Dia** | `int` | Día de la medición. |
| **Hora_10min** | `nvarchar` | Hora redondeada (ej. 14:10). |
| **FechaHora_Original** | `datetime` | Timestamp exacto (Zona Horaria Colombia). |
| **Variable** | `nvarchar` | Nombre de la variable (tempc_sht). |
| **Valor** | `float` | Valor numérico medido. |

## ⚠️ Solución de Problemas

* **Error: `DataSource name not found and no default driver specified**`:
* Falta instalar el *ODBC Driver 17*. Ver sección Requisitos.


* **Error de Conexión SQL (Named Pipes / TCP)**:
* Verifique que el servidor SQL acepte conexiones remotas y que el firewall permita el puerto 1433.


* **Tablas Duplicadas / Datos Dobles**:
* El script usa `append` (agregar). Si se ejecuta varias veces para el mismo rango de tiempo, los datos se duplicarán. Se recomienda limpiar la tabla o ejecutar solo para datos nuevos.



---

**Desarrollado para:** VETO - Excelencia Operacional.
**Última Actualización:** Enero 2026.