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

def guardar_sentimiento_producto(
    idproducto,
    comentario,
    sentimiento,
    puntaje,
    usuario="Anonimo"
):
    """Guarda una opinion analizada sobre un producto"""
    try:
        with engine.begin() as conn:
            conn.exec_driver_sql(
                """
                INSERT INTO sentimientos_productos
                (
                    Idproducto,
                    Comentario,
                    Sentimiento,
                    Puntaje,
                    Usuario,
                    Fecha
                )
                VALUES (%s, %s, %s, %s, %s, NOW())
                """,
                (
                    int(idproducto),
                    comentario,
                    sentimiento,
                    float(puntaje),
                    usuario
                )
            )

        return True

    except Exception as e:
        print("Error guardando sentimiento:", e)
        return False


def obtener_sentimientos_producto(idproducto):
    """Obtiene todas las opiniones de un producto"""
    try:
        return pd.read_sql(
            """
            SELECT
                sp.Id_sentimiento,
                sp.Idproducto,
                p.Nombre AS Producto,
                sp.Comentario,
                sp.Sentimiento,
                sp.Puntaje,
                sp.Usuario,
                sp.Fecha
            FROM sentimientos_productos sp
            INNER JOIN productos p ON p.Idproducto = sp.Idproducto
            WHERE sp.Idproducto = %s
            ORDER BY sp.Fecha DESC
            """,
            engine,
            params=(int(idproducto),)
        )

    except Exception as e:
        print("Error obteniendo sentimientos del producto:", e)
        return pd.DataFrame()


def obtener_resumen_sentimientos():
    """Obtiene resumen general de sentimientos por producto"""
    try:
        return pd.read_sql(
            """
            SELECT
                p.Idproducto,
                p.Nombre AS Producto,
                COUNT(sp.Id_sentimiento) AS Total_opiniones,
                SUM(CASE WHEN sp.Sentimiento = 'Positivo' THEN 1 ELSE 0 END) AS Positivos,
                SUM(CASE WHEN sp.Sentimiento = 'Neutral' THEN 1 ELSE 0 END) AS Neutrales,
                SUM(CASE WHEN sp.Sentimiento = 'Negativo' THEN 1 ELSE 0 END) AS Negativos,
                ROUND(AVG(sp.Puntaje), 2) AS Puntaje_promedio,
                CASE
                    WHEN AVG(sp.Puntaje) >= 0.70 THEN 'Producto bien valorado'
                    WHEN AVG(sp.Puntaje) <= 0.35 THEN 'Producto criticado'
                    ELSE 'Producto aceptable'
                END AS Estado_producto
            FROM productos p
            INNER JOIN sentimientos_productos sp ON sp.Idproducto = p.Idproducto
            GROUP BY p.Idproducto, p.Nombre
            ORDER BY Puntaje_promedio DESC
            """,
            engine
        )

    except Exception as e:
        print("Error obteniendo resumen de sentimientos:", e)
        return pd.DataFrame()


def obtener_top_productos_queridos():
    """Obtiene productos con mejor sentimiento"""
    try:
        return pd.read_sql(
            """
            SELECT
                p.Nombre AS Producto,
                COUNT(sp.Id_sentimiento) AS Total_opiniones,
                ROUND(AVG(sp.Puntaje), 2) AS Puntaje_promedio
            FROM sentimientos_productos sp
            INNER JOIN productos p ON p.Idproducto = sp.Idproducto
            GROUP BY p.Idproducto, p.Nombre
            HAVING COUNT(sp.Id_sentimiento) > 0
            ORDER BY Puntaje_promedio DESC
            LIMIT 10
            """,
            engine
        )

    except Exception as e:
        print("Error obteniendo productos queridos:", e)
        return pd.DataFrame()


def obtener_top_productos_criticados():
    """Obtiene productos con peor sentimiento"""
    try:
        return pd.read_sql(
            """
            SELECT
                p.Nombre AS Producto,
                COUNT(sp.Id_sentimiento) AS Total_opiniones,
                ROUND(AVG(sp.Puntaje), 2) AS Puntaje_promedio
            FROM sentimientos_productos sp
            INNER JOIN productos p ON p.Idproducto = sp.Idproducto
            GROUP BY p.Idproducto, p.Nombre
            HAVING COUNT(sp.Id_sentimiento) > 0
            ORDER BY Puntaje_promedio ASC
            LIMIT 10
            """,
            engine
        )

    except Exception as e:
        print("Error obteniendo productos criticados:", e)
        return pd.DataFrame()