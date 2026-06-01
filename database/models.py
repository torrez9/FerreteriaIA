import pandas as pd
from database.connection import engine

def obtener_clientes():
    """Obtiene todos los clientes"""
    try:
        return pd.read_sql("SELECT * FROM clientes", engine)
    except:
        return pd.DataFrame()

def obtener_productos():
    """Obtiene todos los productos"""
    try:
        return pd.read_sql("SELECT * FROM productos", engine)
    except:
        return pd.DataFrame()

def obtener_facturas():
    """Obtiene todas las facturas"""
    try:
        return pd.read_sql("SELECT * FROM facturas", engine)
    except:
        return pd.DataFrame()

def obtener_inventario():
    """Obtiene el inventario con estado de stock"""
    try:
        return pd.read_sql("""
            SELECT 
                p.Nombre,
                p.Idproducto,
                d.Cantidad,
                d.Min_stock,
                CASE 
                    WHEN d.Cantidad <= d.Min_stock THEN 'Bajo Stock'
                    WHEN d.Cantidad <= d.Min_stock * 2 THEN 'Stock Medio'
                    ELSE 'Stock Alto'
                END as Estado_Stock
            FROM detalle_invs d
            INNER JOIN productos p ON p.Idproducto = d.Idproducto
        """, engine)
    except:
        return pd.DataFrame()

def obtener_proveedores():
    """Obtiene todos los proveedores"""
    try:
        return pd.read_sql("SELECT * FROM proveedors", engine)
    except:
        return pd.DataFrame()

def obtener_ventas_por_dia():
    """Obtiene ventas agrupadas por dia"""
    try:
        return pd.read_sql("""
            SELECT 
                DATE(Fecha) as Fecha,
                COUNT(*) as Numero_Ventas,
                SUM(Total) as Total_Ventas
            FROM facturas
            GROUP BY DATE(Fecha)
            ORDER BY Fecha DESC
            LIMIT 30
        """, engine)
    except:
        return pd.DataFrame()