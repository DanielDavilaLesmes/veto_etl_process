import pandas as pd
from sqlalchemy import create_engine, URL
from src.config import get_db_config

def get_engine():
    """Crea el motor de conexión a SQL Server"""
    db_cfg = get_db_config()
    
    if not db_cfg:
        print("[Load] Error: No hay configuración de DB.")
        return None

    try:
        connection_url = URL.create(
            "mssql+pyodbc",
            username=db_cfg.get("username"),
            password=db_cfg.get("password"),
            host=db_cfg.get("server"),
            database=db_cfg.get("database"),
            query={
                "driver": db_cfg.get("driver", "ODBC Driver 17 for SQL Server"),
                "TrustServerCertificate": "yes"
            }
        )
        return create_engine(connection_url, fast_executemany=True)
    except Exception as e:
        print(f"[Load] Error configurando motor SQL: {e}")
        return None

def save_to_sql(df, variable_name):
    """
    Inserta datos en SQL Server.
    Nombre de tabla dinámico: {prefijo}{variable} -> Ej: ind_Veto_tempc_sht
    """
    if df.empty: return

    engine = get_engine()
    if not engine: return

    db_cfg = get_db_config()
    prefix = db_cfg.get("table_prefix", "ind_Veto_")
    
    # Limpiamos el nombre de la variable para usarlo como nombre de tabla
    safe_var = str(variable_name).replace(" ", "_").lower()
    table_name = f"{prefix}{safe_var}"

    print(f"      -> Insertando en tabla SQL: [{table_name}] ...")
    
    try:
        with engine.begin() as connection:
            df.to_sql(
                name=table_name,
                con=connection,
                if_exists='append', # Agrega a los datos existentes
                index=False,
                schema='dbo'
            )
        print(f"      [OK SQL] {len(df)} registros insertados exitosamente.")
        
    except Exception as e:
        print(f"      [ERROR SQL] Fallo inserción en {table_name}: {e}")