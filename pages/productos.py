import streamlit as st
import pandas as pd
from database.models import obtener_productos

st.set_page_config(page_title="Productos - Ferreteria IA", page_icon="", layout="wide")

st.title("Catalogo de Productos")

productos_df = obtener_productos()

if not productos_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Productos", len(productos_df))
    
    with col2:
        st.metric("Categorias", productos_df['Categoria'].nunique() if 'Categoria' in productos_df.columns else "N/A")
    
    st.divider()
    
    # Filtros
    col_filt1, col_filt2 = st.columns(2)
    
    with col_filt1:
        if 'Categoria' in productos_df.columns:
            categoria = st.selectbox("Filtrar por categoria:", ["Todas"] + list(productos_df['Categoria'].unique()))
            if categoria != "Todas":
                productos_df = productos_df[productos_df['Categoria'] == categoria]
    
    st.dataframe(productos_df, use_container_width=True)
else:
    st.info("No hay datos de productos disponibles")