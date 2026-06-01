import streamlit as st
import pandas as pd
from database.models import obtener_inventario, obtener_facturas

st.set_page_config(page_title="DSS - Decision Support System", page_icon="", layout="wide")

st.title("Sistema de Apoyo a Decisiones (DSS)")
st.markdown("Decisiones inteligentes basadas en datos")

inventario_df = obtener_inventario()
facturas_df = obtener_facturas()

st.subheader("Alertas del Sistema")

# Alertas de inventario
if not inventario_df.empty:
    if 'Cantidad' in inventario_df.columns and 'Min_stock' in inventario_df.columns:
        productos_criticos = inventario_df[inventario_df['Cantidad'] <= inventario_df['Min_stock']]
        
        for _, producto in productos_criticos.iterrows():
            nombre = producto['Nombre'] if 'Nombre' in producto.index else "Producto desconocido"
            st.error(f"ALERTA CRITICA: {nombre} - Stock: {producto['Cantidad']} (Minimo: {producto['Min_stock']})")
    elif 'Cantidad' in inventario_df.columns:
        productos_criticos = inventario_df[inventario_df['Cantidad'] <= 10]
        for _, producto in productos_criticos.iterrows():
            nombre = producto['Nombre'] if 'Nombre' in producto.index else "Producto desconocido"
            st.warning(f"ALERTA: {nombre} - Stock bajo: {producto['Cantidad']} unidades")

st.divider()

# Recomendaciones
st.subheader("Recomendaciones Automaticas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Compras Recomendadas")
    if not inventario_df.empty:
        if 'Cantidad' in inventario_df.columns and 'Min_stock' in inventario_df.columns:
            productos_bajos = inventario_df[inventario_df['Cantidad'] <= inventario_df['Min_stock'] * 1.5]
            for _, prod in productos_bajos.head(5).iterrows():
                cantidad_recomendada = prod['Min_stock'] * 2 - prod['Cantidad']
                if cantidad_recomendada > 0:
                    nombre = prod['Nombre'] if 'Nombre' in prod.index else "Producto"
                    st.write(f"- {nombre}: Comprar {int(cantidad_recomendada)} unidades")
        elif 'Cantidad' in inventario_df.columns:
            productos_bajos = inventario_df[inventario_df['Cantidad'] <= 20]
            for _, prod in productos_bajos.head(5).iterrows():
                nombre = prod['Nombre'] if 'Nombre' in prod.index else "Producto"
                st.write(f"- {nombre}: Stock actual {prod['Cantidad']} - Recomendar compra")

with col2:
    st.markdown("#### Analisis de Ventas")
    if not facturas_df.empty and 'Total' in facturas_df.columns:
        promedio_ventas = facturas_df['Total'].mean()
        st.metric("Ticket Promedio", f"C$ {promedio_ventas:,.2f}")
        
        if promedio_ventas < 200:
            st.info("Recomendacion: Implementar promociones para aumentar ticket")
        else:
            st.success("Ticket promedio optimo")
    else:
        st.info("No hay datos de ventas suficientes")

st.divider()

# Decisiones estrategicas
st.subheader("Decisiones Estrategicas")

decision = st.selectbox(
    "Analisis estrategico:",
    ["Optimizacion de inventario", "Estrategia de precios", "Promociones"]
)

if decision == "Optimizacion de inventario":
    if not inventario_df.empty:
        total_productos = len(inventario_df)
        st.info(f"Recomendacion: Establecer puntos de reorden automaticos para {total_productos} productos")
    else:
        st.info("Recomendacion: Implementar sistema de gestion de inventario")
elif decision == "Estrategia de precios":
    if not facturas_df.empty:
        ventas_totales = facturas_df['Total'].sum() if 'Total' in facturas_df.columns else 0
        st.info(f"Recomendacion: Revisar precios - Ventas totales: C$ {ventas_totales:,.2f}")
    else:
        st.info("Recomendacion: Analizar competencia y ajustar precios")
else:
    st.info("Recomendacion: Ofrecer descuentos en productos de baja rotacion")