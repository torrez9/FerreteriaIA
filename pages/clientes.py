import streamlit as st
import pandas as pd
from database.models import obtener_clientes

st.set_page_config(page_title="Clientes - Ferreteria IA", page_icon="", layout="wide")

st.title("Gestion de Clientes")

clientes_df = obtener_clientes()

if not clientes_df.empty:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.metric("Total Clientes", len(clientes_df))
    
    with col2:
        st.metric("Ultimos Registros", len(clientes_df[clientes_df.index > len(clientes_df)-5]) if len(clientes_df) > 5 else len(clientes_df))
    
    st.divider()
    
    # Buscador
    busqueda = st.text_input("Buscar cliente:", placeholder="Nombre, email o telefono...")
    
    if busqueda:
        mask = clientes_df.apply(lambda row: busqueda.lower() in str(row.values).lower(), axis=1)
        clientes_filtrados = clientes_df[mask]
        st.dataframe(clientes_filtrados, use_container_width=True)
    else:
        st.dataframe(clientes_df, use_container_width=True)
else:
    st.info("No hay datos de clientes disponibles")