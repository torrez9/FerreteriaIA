import pandas as pd
from database.connection import engine

def obtener_clientes():
    return pd.read_sql(
        "SELECT * FROM clientes",
        engine
    )

def obtener_productos():
    return pd.read_sql(
        "SELECT * FROM productos",
        engine
    )

def obtener_facturas():
    return pd.read_sql(
        "SELECT * FROM facturas",
        engine
    )

def obtener_inventario():
    return pd.read_sql("""
        SELECT
            p.Nombre,
            d.Cantidad,
            d.Min_stock
        FROM detalle_invs d
        INNER JOIN productos p
            ON p.Idproducto = d.Idproducto
    """, engine)

def obtener_proveedores():
    return pd.read_sql(
        "SELECT * FROM proveedors",
        engine
    )