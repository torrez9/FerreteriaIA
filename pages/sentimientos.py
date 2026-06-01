import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analisis de Sentimiento - Ferreteria IA", page_icon="", layout="wide")

st.title("Analisis de Sentimiento")
st.markdown("Interpretacion de opiniones y comentarios de clientes")

# Palabras clave
palabras_positivas = ['excelente', 'bueno', 'perfecto', 'rapido', 'calidad', 'recomiendo', 
                      'satisfecho', 'buen', 'genial', 'fantastico', 'util', 'facil']
palabras_negativas = ['malo', 'pesimo', 'lento', 'defectuoso', 'roto', 'caro', 
                      'problema', 'queja', 'decepcionado', 'tarde', 'falla']

def analizar_sentimiento(texto):
    """Analiza el sentimiento de un texto"""
    if not texto or texto.strip() == "":
        return {'sentimiento': 'neutral', 'puntuacion': 0.5}
    
    texto_limpio = texto.lower()
    
    positivas = sum(1 for palabra in palabras_positivas if palabra in texto_limpio)
    negativas = sum(1 for palabra in palabras_negativas if palabra in texto_limpio)
    
    total = positivas + negativas
    if total == 0:
        puntuacion = 0.5
    else:
        puntuacion = positivas / total
    
    if puntuacion >= 0.7:
        sentimiento = "positivo"
    elif puntuacion <= 0.3:
        sentimiento = "negativo"
    else:
        sentimiento = "neutral"
    
    return {'sentimiento': sentimiento, 'puntuacion': puntuacion, 'positivas': positivas, 'negativas': negativas}

# Interfaz
col1, col2 = st.columns([2, 1])

with col1:
    comentario = st.text_area("Ingrese un comentario del cliente:", 
                              height=150,
                              placeholder="Ejemplo: El producto es excelente, muy buena calidad...")
    
    if st.button("Analizar Sentimiento", use_container_width=True):
        if comentario:
            resultado = analizar_sentimiento(comentario)
            
            if resultado['sentimiento'] == 'positivo':
                st.success(f"✅ SENTIMIENTO POSITIVO - {resultado['puntuacion']:.1%}")
                st.balloons()
            elif resultado['sentimiento'] == 'negativo':
                st.error(f"❌ SENTIMIENTO NEGATIVO - {resultado['puntuacion']:.1%}")
            else:
                st.info(f" SENTIMIENTO NEUTRAL - {resultado['puntuacion']:.1%}")
            
            st.markdown(f"**Palabras positivas:** {resultado['positivas']}")
            st.markdown(f"**Palabras negativas:** {resultado['negativas']}")

with col2:
    st.markdown("### Comentarios de ejemplo")
    ejemplos = [
        "Excelente producto, muy buena calidad",
        "El envio fue muy lento y el producto llego dañado",
        "Precio justo, calidad aceptable"
    ]
    
    for ej in ejemplos:
        if st.button(ej[:30] + "...", key=ej):
            resultado = analizar_sentimiento(ej)
            st.write(f"**Sentimiento:** {resultado['sentimiento'].upper()}")

# Estadisticas historicas
st.divider()
st.subheader("Estadisticas de Sentimiento")

# Datos simulados para grafico
sentimientos_data = pd.DataFrame({
    'Sentimiento': ['Positivo', 'Neutral', 'Negativo'],
    'Porcentaje': [65, 20, 15]
})

fig = px.pie(sentimientos_data, values='Porcentaje', names='Sentimiento',
             title="Distribucion General de Sentimientos",
             color_discrete_sequence=['#10b981', '#6b7280', '#ef4444'])
st.plotly_chart(fig, use_container_width=True)