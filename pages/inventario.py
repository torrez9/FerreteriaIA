import streamlit as st
import pandas as pd
import plotly.express as px
from database.models import obtener_inventario, obtener_productos

st.set_page_config(page_title="Inventario - Ferreteria IA", page_icon="", layout="wide")

st.title("Control de Inventario")

inventario_df = obtener_inventario()

if not inventario_df.empty:
    # Metricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Productos", len(inventario_df))
    with col2:
        stock_bajo = len(inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock'])
        st.metric("Stock Critico", stock_bajo, delta="-Alerta" if stock_bajo > 0 else "Normal")
    with col3:
        total_unidades = inventario_df['Cantidad'].sum()
        st.metric("Total Unidades", f"{total_unidades:,}")
    
    st.divider()
    
    # Productos con stock bajo
    st.subheader("Productos con Stock Bajo")
    productos_criticos = inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock']
    
    if not productos_criticos.empty:
        st.warning(f"Se encontraron {len(productos_criticos)} productos con stock bajo")
        st.dataframe(productos_criticos, use_container_width=True)
    else:
        st.success("No hay productos con stock critico")
    
    st.divider()
    
    # Tabla completa
    st.subheader("Inventario Completo")
    st.dataframe(inventario_df, use_container_width=True)
else:
    st.info("No hay datos de inventario disponibles")