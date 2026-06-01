import streamlit as st
from database.models import obtener_clientes

st.title("👥 Clientes")

clientes = obtener_clientes()

st.dataframe(
    clientes,
    use_container_width=True
)