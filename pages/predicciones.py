import streamlit as st
import pandas as pd

from ml.predictor import predecir

st.title("📈 Predicción de Ventas")

valor = st.number_input(
    "Valor de prueba",
    0
)

if st.button("Predecir"):

    datos = pd.DataFrame({
        "valor":[valor]
    })

    resultado = predecir(datos)

    st.success(
        f"Predicción: {resultado[0]}"
    )