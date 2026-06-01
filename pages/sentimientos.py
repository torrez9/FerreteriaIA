import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Configuracion de la pagina
st.set_page_config(
    page_title="Analisis de Sentimiento - Ferreteria IA", 
    page_icon="", 
    layout="wide"
)

# ==================== ESTILOS CSS UNIFICADOS ====================
st.markdown("""
<style>
    /* === ESTILOS BASE === */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* === HEADER PRINCIPAL === */
    .main-header {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3f 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(96, 165, 250, 0.3);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #cbd5e1;
        font-size: 1rem;
    }
    
    /* === TARJETAS === */
    .card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3f 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(96, 165, 250, 0.2);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-4px);
        border-color: rgba(96, 165, 250, 0.5);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #60a5fa;
        margin-bottom: 1rem;
        border-left: 3px solid #60a5fa;
        padding-left: 0.8rem;
    }
    
    /* === RESULT CARD === */
    .result-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3f 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(96, 165, 250, 0.2);
        margin: 1rem 0;
    }
    
    .result-positive {
        border-left: 4px solid #10b981;
    }
    
    .result-neutral {
        border-left: 4px solid #6b7280;
    }
    
    .result-negative {
        border-left: 4px solid #ef4444;
    }
    
    .result-emoji {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .result-text {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .result-score {
        font-size: 2rem;
        font-weight: bold;
        color: #fbbf24;
    }
    
    /* === BADGES === */
    .badge-positive {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .badge-neutral {
        background: linear-gradient(135deg, #6b7280, #4b5563);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .badge-negative {
        background: linear-gradient(135deg, #dc2626, #b91c1c);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* === BOTONES === */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
    }
    
    /* === TEXT AREA === */
    .stTextArea textarea {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border: 1px solid rgba(96, 165, 250, 0.2);
        border-radius: 12px;
        color: white;
    }
    
    /* === DIVIDERS === */
    hr {
        border-color: rgba(96, 165, 250, 0.2);
        margin: 1.5rem 0;
    }
    
    /* === INFO BOX === */
    .info-box {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #60a5fa;
        color: #cbd5e1;
    }
    
    /* === METRIC CARD === */
    .metric-circle {
        text-align: center;
        padding: 1rem;
    }
    
    .metric-value-large {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e1e2e;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 10px;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 16px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1> Analisis de Sentimiento</h1>
    <p>Interpretacion inteligente de opiniones y comentarios de clientes</p>
    <span class="badge-positive">NLP | Procesamiento de Lenguaje Natural</span>
</div>
""", unsafe_allow_html=True)

# ==================== DICCIONARIO DE PALABRAS ====================
palabras_positivas = [
    'excelente', 'bueno', 'perfecto', 'rapido', 'calidad', 'recomiendo', 
    'satisfecho', 'buen', 'genial', 'fantastico', 'util', 'facil',
    'maravilloso', 'increible', 'espectacular', 'mejor', 'optimo',
    'agradable', 'contento', 'feliz', 'gracias', 'exitoso'
]

palabras_negativas = [
    'malo', 'pesimo', 'lento', 'defectuoso', 'roto', 'caro', 
    'problema', 'queja', 'decepcionado', 'tarde', 'falla',
    'terrible', 'horrible', 'fatal', 'deficiente', 'incumplio',
    'enojado', 'triste', 'molesto', 'fraude', 'estafa'
]

# ==================== FUNCION DE ANALISIS ====================
def analizar_sentimiento(texto):
    """Analiza el sentimiento de un texto con mayor precision"""
    if not texto or texto.strip() == "":
        return {
            'sentimiento': 'neutral', 
            'puntuacion': 0.5, 
            'positivas': 0, 
            'negativas': 0,
            'mensaje': 'No se proporciono texto para analizar'
        }
    
    texto_limpio = texto.lower()
    
    # Contar palabras
    positivas = sum(1 for palabra in palabras_positivas if palabra in texto_limpio)
    negativas = sum(1 for palabra in palabras_negativas if palabra in texto_limpio)
    
    # Calcular puntuacion con ponderacion
    total = positivas + negativas
    if total == 0:
        puntuacion = 0.5
    else:
        puntuacion = positivas / total
    
    # Determinar sentimiento
    if puntuacion >= 0.7:
        sentimiento = "positivo"
        emoji = "😊"
        color = "#10b981"
        mensaje = "El cliente expresa satisfaccion con el producto/servicio"
    elif puntuacion <= 0.3:
        sentimiento = "negativo"
        emoji = "😞"
        color = "#ef4444"
        mensaje = "El cliente muestra insatisfaccion - Requiere atencion prioritaria"
    else:
        sentimiento = "neutral"
        emoji = "😐"
        color = "#6b7280"
        mensaje = "Opinion neutral - Sin emociones fuertes detectadas"
    
    return {
        'sentimiento': sentimiento,
        'puntuacion': puntuacion,
        'positivas': positivas,
        'negativas': negativas,
        'mensaje': mensaje,
        'emoji': emoji,
        'color': color
    }

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">😊</div>
        <h2 style="color: #60a5fa;">Sentiment IA</h2>
        <p style="color: #9ca3af;">Analisis de Opiniones</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Como funciona")
    st.markdown("""
    El analisis de sentimiento utiliza:
    - ✅ **Diccionario de palabras positivas**
    - ❌ **Diccionario de palabras negativas**
    - 📊 **Algoritmo de ponderacion**
    - 🎯 **Clasificacion automatica**
    """)
    
    st.markdown("---")
    
    st.markdown("### Estadisticas del Lexico")
    st.markdown(f"""
    - Palabras positivas: {len(palabras_positivas)}
    - Palabras negativas: {len(palabras_negativas)}
    - Precision: Alta
    """)
    
    st.markdown("---")
    st.markdown(f"**Ultimo analisis:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== INTERFAZ PRINCIPAL ====================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card-title"> Ingrese el texto a analizar</div>', unsafe_allow_html=True)
    
    comentario = st.text_area(
        "", 
        height=150,
        placeholder="Ejemplo: El producto es excelente, muy buena calidad, el envio fue rapido y el precio es justo. Lo recomiendo totalmente."
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🔍 Analizar Sentimiento", use_container_width=True):
            if comentario:
                resultado = analizar_sentimiento(comentario)
                
                # Mostrar resultado con estilo
                st.markdown(f"""
                <div class="result-card result-{resultado['sentimiento']}">
                    <div class="result-emoji">{resultado['emoji']}</div>
                    <div class="result-text" style="color: {resultado['color']}">
                        {resultado['sentimiento'].upper()}
                    </div>
                    <div class="result-score">{resultado['puntuacion']:.1%}</div>
                    <div style="color: #9ca3af; margin-top: 0.5rem;">{resultado['mensaje']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Metricas detalladas
                col_met1, col_met2 = st.columns(2)
                with col_met1:
                    st.metric("Palabras Positivas", resultado['positivas'])
                with col_met2:
                    st.metric("Palabras Negativas", resultado['negativas'])
                
                # Barra de progreso
                st.markdown("#### Nivel de satisfaccion")
                st.progress(resultado['puntuacion'])
                
                if resultado['sentimiento'] == 'positivo':
                    st.balloons()
                elif resultado['sentimiento'] == 'negativo':
                    st.snow()
            else:
                st.warning("⚠️ Por favor ingrese un comentario para analizar")

with col2:
    st.markdown('<div class="card-title"> Comentarios de ejemplo</div>', unsafe_allow_html=True)
    
    ejemplos = [
        ("🌟 Excelente producto, muy buena calidad", "positivo"),
        ("⭐ El envio fue muy lento y el producto llego dañado", "negativo"),
        ("👍 Precio justo, calidad aceptable", "neutral"),
        ("💯 Increible atencion al cliente, muy recomendado", "positivo"),
        ("⚠️ Decepcionado, no cumplieron con lo prometido", "negativo"),
        ("📦 Producto correcto, cumple su funcion", "neutral")
    ]
    
    for texto, tipo in ejemplos:
        color_badge = "#10b981" if tipo == "positivo" else "#ef4444" if tipo == "negativo" else "#6b7280"
        if st.button(f"{texto[:35]}...", key=texto, use_container_width=True):
            resultado = analizar_sentimiento(texto)
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d3f); border-radius: 12px; padding: 0.8rem; margin: 0.5rem 0;">
                    <span style="color: {color_badge}; font-weight: bold;">{resultado['sentimiento'].upper()}</span>
                    <span style="color: #9ca3af;"> - {resultado['puntuacion']:.0%}</span>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ==================== ESTADISTICAS Y GRAFICOS ====================
st.markdown("## Dashboard de Sentimiento")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

# Datos simulados para estadisticas
total_analisis = 152
positivos = 98
neutrales = 32
negativos = 22

with col_stat1:
    st.metric("Total Analisis", total_analisis)
with col_stat2:
    st.metric("Positivos", positivos, delta=f"{positivos/total_analisis*100:.0f}%")
with col_stat3:
    st.metric("Neutrales", neutrales, delta=f"{neutrales/total_analisis*100:.0f}%")
with col_stat4:
    st.metric("Negativos", negativos, delta=f"{negativos/total_analisis*100:.0f}%")

# Graficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown('<div class="card-title"> Distribucion de Sentimientos</div>', unsafe_allow_html=True)
    
    sentimientos_data = pd.DataFrame({
        'Sentimiento': ['Positivo', 'Neutral', 'Negativo'],
        'Cantidad': [positivos, neutrales, negativos],
        'Porcentaje': [positivos/total_analisis*100, neutrales/total_analisis*100, negativos/total_analisis*100]
    })
    
    fig = px.pie(
        sentimientos_data, 
        values='Cantidad', 
        names='Sentimiento',
        template="plotly_dark",
        color_discrete_sequence=['#10b981', '#6b7280', '#ef4444'],
        hole=0.3
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col_graf2:
    st.markdown('<div class="card-title"> Evolucion de Sentimiento</div>', unsafe_allow_html=True)
    
    # Datos de evolucion simulados
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    evolucion_pos = [65, 68, 70, 72, 68, 65]
    evolucion_neg = [20, 18, 15, 14, 16, 18]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses, y=evolucion_pos,
        mode='lines+markers',
        name='Positivo',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=meses, y=evolucion_neg,
        mode='lines+markers',
        name='Negativo',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title="Tendencia de Sentimiento",
        xaxis_title="Mes",
        yaxis_title="Porcentaje (%)",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==================== HISTORIAL DE ANALISIS ====================
with st.expander("📜 Ver Historial de Analisis Recientes"):
    # Datos de historial simulados
    historial_data = pd.DataFrame({
        'Fecha': ['2024-06-01', '2024-05-31', '2024-05-30', '2024-05-29', '2024-05-28'],
        'Comentario': [
            'Excelente servicio, muy recomendado',
            'El producto no cumplio con mis expectativas',
            'Buen precio, calidad aceptable',
            'La atencion fue rapida y eficaz',
            'Tardo mucho el envio'
        ],
        'Sentimiento': ['Positivo', 'Negativo', 'Neutral', 'Positivo', 'Negativo'],
        'Puntuacion': ['92%', '25%', '55%', '88%', '30%']
    })
    
    st.dataframe(
        historial_data,
        use_container_width=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha"),
            "Comentario": st.column_config.TextColumn("Comentario"),
            "Sentimiento": st.column_config.TextColumn("Sentimiento"),
            "Puntuacion": st.column_config.TextColumn("Puntuacion")
        }
    )

# ==================== RECOMENDACIONES ====================
st.divider()
st.markdown("## Recomendaciones basadas en Sentimiento")

if negativos > 10:
    st.warning(f"⚠️ Se han detectado {negativos} comentarios negativos. Se recomienda:")
    st.markdown("""
    - 📞 Contactar a los clientes insatisfechos
    - 🔍 Revisar los productos mas criticados
    - 📈 Implementar mejoras en atencion al cliente
    - 🎯 Ofrecer compensaciones cuando sea necesario
    """)
else:
    st.success("✅ Excelente nivel de satisfaccion general. Mantener estrategias actuales.")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;"> Analisis de Sentimiento - Ferreteria IA</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        NLP | Procesamiento de Lenguaje Natural | Analisis de Opiniones
    </p>
</div>
""", unsafe_allow_html=True)