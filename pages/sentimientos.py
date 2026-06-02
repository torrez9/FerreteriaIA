import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database.models import (
    obtener_productos,
    guardar_sentimiento_producto,
    obtener_sentimientos_producto,
    obtener_resumen_sentimientos,
    obtener_top_productos_queridos,
    obtener_top_productos_criticados
)

st.set_page_config(
    page_title="Análisis de Sentimiento - Ferretería IA",
    page_icon="😊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
}
.main-header {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3f 100%);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(96, 165, 250, 0.3);
}
.main-header h1 {
    color: #60a5fa;
    font-size: 2.5rem;
}
.main-header p {
    color: #cbd5e1;
}
.stButton button {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    width: 100%;
}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
    border-radius: 16px;
    padding: 1rem;
    border: 1px solid rgba(96, 165, 250, 0.2);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>😊 Análisis de Sentimiento</h1>
    <p>Registro y análisis inteligente de opiniones por producto</p>
</div>
""", unsafe_allow_html=True)


palabras_positivas = [
    "excelente", "bueno", "buen", "calidad", "recomiendo", "perfecto",
    "rápido", "rapido", "útil", "util", "me gusta", "gustó", "gusto",
    "satisfecho", "duradero", "barato", "funciona", "eficiente"
]

palabras_negativas = [
    "malo", "mala", "pésimo", "pesimo", "defectuoso", "roto",
    "caro", "falla", "falló", "fallo", "problema", "decepcionado",
    "no sirve", "mala calidad", "lento", "horrible", "dañado", "danado"
]


def analizar_sentimiento_diccionario(texto):
    if not texto or texto.strip() == "":
        return "Neutral", 0.50, 0, 0

    texto = texto.lower().strip()

    positivas = sum(1 for palabra in palabras_positivas if palabra in texto)
    negativas = sum(1 for palabra in palabras_negativas if palabra in texto)

    if positivas > negativas:
        return "Positivo", 0.85, positivas, negativas

    if negativas > positivas:
        return "Negativo", 0.20, positivas, negativas

    return "Neutral", 0.50, positivas, negativas


def analizar_sentimiento(texto):
    return analizar_sentimiento_diccionario(texto)
productos_df = obtener_productos()

if productos_df.empty:
    st.error("No se encontraron productos en la base de datos.")
    st.stop()

productos_df["Etiqueta"] = productos_df["Idproducto"].astype(str) + " - " + productos_df["Nombre"].astype(str)

st.markdown("## Registrar opinión de cliente")

col1, col2 = st.columns([2, 1])

with col1:
    producto_seleccionado = st.selectbox(
        "Seleccione un producto",
        productos_df["Etiqueta"].tolist()
    )

    idproducto = int(producto_seleccionado.split(" - ")[0])

    usuario = st.text_input(
        "Nombre de la persona",
        placeholder="Ejemplo: Cliente anónimo"
    )

    comentario = st.text_area(
        "Comentario sobre el producto",
        height=140,
        placeholder="Ejemplo: Me gustó mucho este producto, es de buena calidad."
    )

    if st.button("Analizar y guardar opinión"):
        if not comentario.strip():
            st.warning("Escriba un comentario antes de guardar.")
        else:
            sentimiento, puntaje, positivas, negativas = analizar_sentimiento(comentario)

            guardado = guardar_sentimiento_producto(
                idproducto=idproducto,
                comentario=comentario,
                sentimiento=sentimiento,
                puntaje=puntaje,
                usuario=usuario if usuario.strip() else "Anonimo"
            )

            if guardado:
                st.success(f"Opinión guardada correctamente. Sentimiento detectado: {sentimiento}")
                st.metric("Puntaje", f"{puntaje:.0%}")
                st.write(f"Palabras positivas detectadas: {positivas}")
                st.write(f"Palabras negativas detectadas: {negativas}")
            else:
                st.error("No se pudo guardar la opinión.")

with col2:
    st.markdown("### Resultado esperado")
    st.info("""
    El sistema acumula votos por producto y calcula si el producto es:
    
    - Bien valorado
    - Aceptable
    - Criticado
    """)

st.divider()

st.markdown("## Resumen general de sentimientos")

resumen_df = obtener_resumen_sentimientos()

if not resumen_df.empty:
    total_opiniones = int(resumen_df["Total_opiniones"].sum())
    promedio_general = resumen_df["Puntaje_promedio"].mean()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total opiniones", total_opiniones)

    with c2:
        st.metric("Puntaje promedio", f"{promedio_general:.0%}")

    with c3:
        st.metric("Productos evaluados", len(resumen_df))

    st.dataframe(resumen_df, use_container_width=True)

    fig = px.bar(
        resumen_df.head(10),
        x="Producto",
        y="Puntaje_promedio",
        color="Estado_producto",
        title="Top productos según sentimiento",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Todavía no hay opiniones registradas.")

st.divider()

col_top1, col_top2 = st.columns(2)

with col_top1:
    st.markdown("## Productos más queridos")
    queridos_df = obtener_top_productos_queridos()

    if not queridos_df.empty:
        st.dataframe(queridos_df, use_container_width=True)
    else:
        st.info("Aún no hay datos suficientes.")

with col_top2:
    st.markdown("## Productos más criticados")
    criticados_df = obtener_top_productos_criticados()

    if not criticados_df.empty:
        st.dataframe(criticados_df, use_container_width=True)
    else:
        st.info("Aún no hay datos suficientes.")

st.divider()

st.markdown("## Historial por producto")

producto_historial = st.selectbox(
    "Seleccione producto para ver historial",
    productos_df["Etiqueta"].tolist(),
    key="historial_producto"
)

id_historial = int(producto_historial.split(" - ")[0])
historial_df = obtener_sentimientos_producto(id_historial)

if not historial_df.empty:
    st.dataframe(historial_df, use_container_width=True)
else:
    st.info("Este producto todavía no tiene opiniones registradas.")