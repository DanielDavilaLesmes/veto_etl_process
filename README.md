
# VETO ETL Process: Ubidots a Excel

Este proyecto implementa un proceso **ETL (Extracción, Transformación y Carga)** automatizado en Python para descargar datos históricos de sensores desde la plataforma **Ubidots**, normalizarlos temporalmente y generar reportes consolidados en formato Excel.

El sistema está diseñado para manejar múltiples dispositivos (Pasillos, Sondas, etc.) y agrupar la información por **Tipo de Variable**, facilitando el análisis masivo de datos.

## 📋 Características Principales

* **Extracción Modular:** Conexión robusta a la API v1.6 de Ubidots con manejo de paginación.
* **Normalización Temporal:** Conversión automática de timestamps Unix a zona horaria local (Colombia) y creación de *buckets* de tiempo de 10 minutos.
* **Enriquecimiento de Datos:** Generación de llaves compuestas (`Llave_Comun`) y desglose de fechas (Año, Mes, Día, Hora).
* **Consolidación por Variable:** Genera un archivo `.xlsx` único por cada variable (ej. `tempc_sht.xlsx`) que contiene la data de todos los dispositivos configurados.
* **Configuración Externa:** Gestión de dispositivos y credenciales mediante archivo JSON para seguridad y escalabilidad.

## 📂 Estructura del Proyecto

```text
VETO_ETL_PROCESS/
│
├── src/                        # Paquete de código fuente
│   ├── __init__.py
│   ├── config.py               # Lectura de configuración y validaciones
│   ├── extract.py              # Lógica de conexión a la API (Request/Response)
│   ├── transform.py            # Limpieza, zonas horarias y columnas calculadas
│   └── load.py                 # Exportación a archivos Excel
│
├── config_devices.json         # Archivo de configuración (Dispositivos y Sensores)
├── requirements.txt            # Dependencias del proyecto
├── run_etl.py                  # Orquestador principal
└── README.md                   # Documentación

```

## ⚙️ Requisitos Previos

* **Python 3.8** o superior.
* Conexión a internet (Acceso a `industrial.api.ubidots.com`).
* Credenciales de Ubidots (Tokens y API Labels).

### Instalación de Dependencias

Ejecute el siguiente comando para instalar las librerías necesarias:

```bash
pip install pandas requests openpyxl

```

*(O use el archivo requirements.txt si ya lo generó)*:

```bash
pip install -r requirements.txt

```

## 🔧 Configuración (`config_devices.json`)

El sistema se alimenta de un archivo JSON en la raíz del proyecto. Debe seguir estrictamente esta estructura:

```json
{
  "sensors": [
    "tempc_sht",
    "humidity",
    "bat_status"
  ],
  "devices": [
    {
      "device_name": "P001",
      "device_category": "Pasillos",
      "device_api_label": "eui-a84041f5a186de1a",
      "device_ID": "690df11ec531062ed377159d",
      "device_token": "BBUS-XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    },
    {
      "device_name": "Sonda 1",
      "device_category": "Sondas",
      "device_api_label": "eui-b123456789abcdef",
      "device_token": "BBUS-YYYYYYYYYYYYYYYYYYYYYYYYYYYY"
    }
  ]
}

```

* **sensors:** Lista de las variables (API Labels) que se buscarán en *todos* los dispositivos.
* **devices:** Lista de objetos con las credenciales específicas de cada dispositivo.

## 🚀 Ejecución

Para iniciar el proceso de extracción y generación de reportes:

```bash
python run_etl.py

```

### Flujo de Ejecución:

1. El script lee la lista de `sensors`.
2. Toma la primera variable (ej. `tempc_sht`).
3. Itera sobre los 43 dispositivos configurados, descargando los últimos 1.000 datos de esa variable específica.
4. Aplica transformaciones (Zona Horaria, Redondeo a 10 min).
5. Consolida toda la información en un DataFrame maestro.
6. Genera el archivo `Resultados_Por_Variable/tempc_sht.xlsx`.
7. Repite el proceso para la siguiente variable.

## 📊 Salida (Output)

Los archivos se generarán automáticamente en la carpeta `Resultados_Por_Variable/`.

**Ejemplo de estructura de columnas en Excel:**

| Llave_Comun | Pasillo | Pasillo_est | Anio | Mes | Dia | Hora_10min | FechaHora_Original | Variable | Valor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202601200000 | Pasillo 1 | P001 | 2026 | 1 | 20 | 00:00 | 2026-01-20 00:01:00 | tempc_sht | -19.2 |
| 202601200010 | Pasillo 1 | P001 | 2026 | 1 | 20 | 00:10 | 2026-01-20 00:11:04 | tempc_sht | -19.1 |

* **Llave_Comun:** Formato `AAAAMMDDHHMM` (Agrupación de 10 min). Útil para cruces de datos.
* **Hora_10min:** Hora redondeada al múltiplo de 10 minutos inferior.

## ⚠️ Notas Técnicas

1. **Límite de Datos:** Actualmente configurado para descargar los últimos 1.000 registros por petición (`page_size=1000`).
2. **Manejo de Errores:**
* Si un dispositivo no tiene una variable específica (ej. "Batería" en un sensor virtual), el script lo omite silenciosamente y continúa con el siguiente.
* Errores de conexión (Timeouts/SSL) son capturados y logueados en consola.



---

**Desarrollado para:** VETO - Proyecto de Excelencia Operacional.
**Fecha de actualización:** Enero 2026.
