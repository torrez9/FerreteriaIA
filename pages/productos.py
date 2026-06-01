import streamlit as st
from database.models import obtener_productos

st.title("📦 Productos")

productos = obtener_productos()

st.dataframe(
    productos,
    use_container_width=True
)