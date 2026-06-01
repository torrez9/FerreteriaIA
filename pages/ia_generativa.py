import streamlit as st
from datetime import datetime
from database.models import obtener_facturas, obtener_inventario

st.set_page_config(page_title="IA Generativa - Ferreteria IA", page_icon="", layout="wide")

st.title("IA Generativa")
st.markdown("Generacion automatica de contenido empresarial")

facturas_df = obtener_facturas()
inventario_df = obtener_inventario()

def generar_reporte_ventas():
    """Genera reporte de ventas automaticamente"""
    if facturas_df.empty:
        return "No hay datos de ventas disponibles"
    
    total_ventas = facturas_df['Total'].sum() if 'Total' in facturas_df.columns else 0
    num_ventas = len(facturas_df)
    
    reporte = f"""
    ========================================
    REPORTE DE VENTAS GENERADO POR IA
    ========================================
    
    Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    RESUMEN:
    - Ventas totales: {num_ventas}
    - Ingresos: C$ {total_ventas:,.2f}
    - Promedio: C$ {total_ventas/num_ventas:,.2f}
    
    ANALISIS:
    El negocio ha generado C$ {total_ventas:,.2f} en {num_ventas} transacciones.
    El ticket promedio es de C$ {total_ventas/num_ventas:,.2f}.
    
    RECOMENDACIONES:
    {'Implementar promociones para aumentar ventas' if num_ventas < 100 else 'Mantener estrategia actual'}
    
    ========================================
    """
    return reporte

def generar_resumen_inventario():
    """Genera resumen del inventario"""
    if inventario_df.empty:
        return "No hay datos de inventario"
    
    total = len(inventario_df)
    stock_bajo = len(inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock']) if 'Estado_Stock' in inventario_df.columns else 0
    
    resumen = f"""
    RESUMEN DE INVENTARIO
    Total productos: {total}
    Productos con stock bajo: {stock_bajo}
    
    Acciones recomendadas:
    - {'Realizar pedidos urgentemente' if stock_bajo > 0 else 'Inventario optimo'}
    - Revisar productos de alta rotacion
    """
    return resumen

# Interfaz
tipo = st.selectbox("Tipo de contenido a generar:", 
                    ["Reporte de Ventas", "Resumen de Inventario", "Correo Promocional"])

if st.button("Generar con IA", use_container_width=True):
    with st.spinner("IA Generativa trabajando..."):
        if tipo == "Reporte de Ventas":
            contenido = generar_reporte_ventas()
        elif tipo == "Resumen de Inventario":
            contenido = generar_resumen_inventario()
        else:
            contenido = """
            Asunto: Oferta Especial - IA Generativa
            
            Estimado cliente,
            
            Nuestro sistema IA ha identificado productos que pueden interesarte.
            
            Por ser cliente frecuente, te ofrecemos 10% descuento.
            
            ¡Te esperamos!
            
            Ferreteria IA
            """
        
        st.code(contenido, language="text")
        
        st.download_button(
            "Descargar Contenido",
            contenido,
            file_name=f"contenido_ia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )