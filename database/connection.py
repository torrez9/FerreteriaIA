from sqlalchemy import create_engine
import pandas as pd

# Conexion a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/bd_fhls")

def get_engine():
    """Retorna el engine de conexion a la base de datos"""
    return engine

def test_connection():
    """Prueba la conexion a la base de datos"""
    try:
        with engine.connect() as conn:
            return True
    except Exception as e:
        print(f"Error de conexion: {e}")
        return False
