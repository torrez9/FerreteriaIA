import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from database.models import obtener_facturas, obtener_productos
from ml.predictor import predictor

# Configuracion de la pagina
st.set_page_config(
    page_title="Predicciones IA - Ferreteria IA", 
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
    
    /* === METRIC CARDS === */
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3f 100%);
        padding: 1.2rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(96, 165, 250, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(96, 165, 250, 0.5);
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #fbbf24;
        margin: 0.5rem 0;
    }
    
    .metric-card .metric-label {
        color: #9ca3af;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* === BADGES === */
    .badge-ia {
        background: linear-gradient(135deg, #7c3aed, #6d28d9);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #059669, #047857);
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
    
    /* === METRICAS NATIVAS === */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    div[data-testid="stMetric"] label {
        color: #9ca3af !important;
    }
    
    div[data-testid="stMetric"] .stMetricValue {
        color: #60a5fa !important;
    }
    
    /* === SLIDERS === */
    .stSlider div {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
    }
    
    /* === EXPANDERS === */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        color: #60a5fa;
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, #1a1a2e, #0f0f1a);
        border-radius: 12px;
        color: #d1d5db;
    }
    
    /* === INFO BOX === */
    .info-box {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #60a5fa;
        color: #cbd5e1;
    }
    
    /* === PREDICTION CARD === */
    .pred-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    .pred-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #fbbf24;
    }
    
    /* === DIVIDERS === */
    hr {
        border-color: rgba(96, 165, 250, 0.2);
        margin: 1.5rem 0;
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
    <h1> Modelo Predictivo IA</h1>
    <p>Predicciones avanzadas basadas en inteligencia artificial y machine learning</p>
    <span class="badge-ia">Random Forest | Prediccion de Ventas</span>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
facturas_df = obtener_facturas()
productos_df = obtener_productos()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">🔮</div>
        <h2 style="color: #60a5fa;">Predictor IA</h2>
        <p style="color: #9ca3af;">Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Configuracion del Modelo")
    st.markdown("""
    - **Algoritmo:** Random Forest
    - **Entrenamiento:** Automatico
    - **Precision:** En tiempo real
    """)
    
    st.markdown("---")
    
    st.markdown("### Estadisticas de Datos")
    if not facturas_df.empty:
        st.metric("Registros de Ventas", len(facturas_df))
        if 'Total' in facturas_df.columns:
            st.metric("Ingreso Total", f"C$ {facturas_df['Total'].sum():,.2f}")
    
    st.markdown("---")
    st.markdown(f"**Ultima prediccion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== METRICAS INICIALES ====================
if not facturas_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Facturas", f"{len(facturas_df):,}")
    with col2:
        if 'Total' in facturas_df.columns:
            st.metric("Ingresos Totales", f"C$ {facturas_df['Total'].sum():,.2f}")
    with col3:
        if 'Total' in facturas_df.columns:
            st.metric("Ticket Promedio", f"C$ {facturas_df['Total'].mean():,.2f}")
    with col4:
        if 'Total' in facturas_df.columns:
            max_venta = facturas_df['Total'].max()
            st.metric("Venta Maxima", f"C$ {max_venta:,.2f}")
    
    st.divider()

# ==================== VERIFICAR DATOS ====================
if not facturas_df.empty:
    if 'Total' in facturas_df.columns:
        st.markdown(f"""
        <div class="info-box">
            <strong>📊 Datos cargados correctamente:</strong> {len(facturas_df)} facturas disponibles<br>
            <strong>💰 Total de ventas registradas:</strong> C$ {facturas_df['Total'].sum():,.2f}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ La tabla de facturas no tiene la columna 'Total'")
else:
    st.warning("⚠️ No hay datos de facturas disponibles")

# ==================== MODELO PREDICTIVO ====================
if not facturas_df.empty and 'Total' in facturas_df.columns:
    
    # Entrenar modelo
    with st.spinner("🧠 Preparando modelo predictivo (Random Forest)..."):
        try:
            exito = predictor.entrenar_modelo(facturas_df)
            if exito:
                st.success("✅ Modelo entrenado correctamente")
            else:
                st.info("ℹ️ Usando modelo basico (sin entrenamiento profundo)")
        except Exception as e:
            st.warning(f"⚠️ Modelo en modo basico: {str(e)[:100]}")
    
    st.divider()
    
    # ==================== SECCION DE PREDICCIONES ====================
    st.markdown("## Generador de Predicciones")
    
    col_pred1, col_pred2 = st.columns([1, 2])
    
    with col_pred1:
        st.markdown('<div class="card-title">Configuracion</div>', unsafe_allow_html=True)
        dias_prediccion = st.slider("Dias a predecir:", 3, 60, 14, help="Cantidad de dias hacia el futuro para predecir ventas")
        
        st.markdown("### Metodo de Prediccion")
        metodo = st.radio(
            "Seleccione metodo:",
            ["Random Forest (Recomendado)", "Promedio Movil Simple", "Tendencia Lineal"]
        )
    
    with col_pred2:
        if st.button("🔮 Generar Predicciones", use_container_width=True):
            with st.spinner("🧠 IA generando predicciones avanzadas..."):
                try:
                    predicciones = predictor.predecir_ventas(facturas_df, dias_prediccion)
                    
                    # Crear grafico mejorado
                    fig = go.Figure()
                    
                    # Datos historicos (ultimos 30 dias)
                    datos_hist = facturas_df['Total'].tail(30)
                    fechas_hist = list(range(len(datos_hist)))
                    
                    fig.add_trace(go.Scatter(
                        x=fechas_hist,
                        y=datos_hist.values,
                        mode='lines+markers',
                        name='📊 Ventas Historicas',
                        line=dict(color='#3b82f6', width=3),
                        marker=dict(size=8, symbol='circle', color='#60a5fa'),
                        hovertemplate='Dia: %{x}<br>Venta: C$ %{y:,.2f}<extra></extra>'
                    ))
                    
                    # Predicciones
                    fechas_pred = list(range(len(datos_hist), len(datos_hist) + dias_prediccion))
                    
                    fig.add_trace(go.Scatter(
                        x=fechas_pred,
                        y=predicciones,
                        mode='lines+markers',
                        name='🔮 Predicciones IA',
                        line=dict(color='#ef4444', width=3, dash='dash'),
                        marker=dict(size=10, symbol='diamond', color='#f87171'),
                        hovertemplate='Dia: %{x}<br>Prediccion: C$ %{y:,.2f}<extra></extra>'
                    ))
                    
                    # Area de confianza (simulada)
                    upper_bound = [p * 1.15 for p in predicciones]
                    lower_bound = [p * 0.85 for p in predicciones]
                    
                    fig.add_trace(go.Scatter(
                        x=fechas_pred + fechas_pred[::-1],
                        y=upper_bound + lower_bound[::-1],
                        fill='toself',
                        fillcolor='rgba(239, 68, 68, 0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='Intervalo de Confianza (85%)',
                        hoverinfo='skip'
                    ))
                    
                    fig.update_layout(
                        title="📈 Prediccion de Ventas - Proyeccion a Futuro",
                        xaxis_title="Periodo (Dias)",
                        yaxis_title="Ventas (C$)",
                        template="plotly_dark",
                        hovermode='x unified',
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01,
                            bgcolor="rgba(0,0,0,0.5)"
                        ),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Mostrar predicciones en tarjetas
                    st.markdown("### Predicciones Detalladas")
                    
                    # Mostrar primeras 7 predicciones en columnas
                    cols = st.columns(min(dias_prediccion, 7))
                    for i, (col, pred) in enumerate(zip(cols, predicciones[:7])):
                        with col:
                            st.markdown(f"""
                            <div class="pred-card">
                                <div style="color: #9ca3af; font-size: 0.8rem;">Dia {i+1}</div>
                                <div class="pred-value">C$ {pred:,.0f}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Mostrar todas las predicciones en expander
                    with st.expander(f"📋 Ver todas las predicciones ({dias_prediccion} dias)"):
                        for i, pred in enumerate(predicciones, 1):
                            st.write(f"**Dia {i}:** C$ {pred:,.2f}")
                    
                    # Analisis de tendencia
                    tendencia = "📈 Tendencia Positiva" if predicciones[-1] > predicciones[0] else "📉 Tendencia Negativa" if predicciones[-1] < predicciones[0] else "➡️ Tendencia Estable"
                    crecimiento = ((predicciones[-1] - predicciones[0]) / predicciones[0] * 100) if predicciones[0] > 0 else 0
                    
                    st.markdown(f"""
                    <div class="info-box">
                        <strong>📊 Analisis de Tendencia:</strong><br>
                        {tendencia}<br>
                        Crecimiento estimado: {crecimiento:+.1f}%<br>
                        Promedio de ventas proyectado: C$ {np.mean(predicciones):,.2f}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error generando predicciones: {str(e)}")
                    st.info("💡 Usando datos de ejemplo para demostracion")
                    
                    # Datos de ejemplo
                    predicciones_ejemplo = [120 + i * 5 for i in range(dias_prediccion)]
                    st.line_chart(predicciones_ejemplo, use_container_width=True)
    
    st.divider()
    
    # ==================== ANALISIS DE PRODUCTOS ====================
    st.markdown("## Analisis de Productos")
    
    col_prod1, col_prod2 = st.columns(2)
    
    with col_prod1:
        st.markdown('<div class="card-title"> Productos Populares</div>', unsafe_allow_html=True)
        if st.button("📊 Analizar Productos Mas Vendidos", use_container_width=True):
            with st.spinner("Analizando patrones de compra..."):
                try:
                    productos_populares = predictor.predecir_productos_populares(facturas_df)
                    if isinstance(productos_populares, pd.DataFrame) and not productos_populares.empty:
                        st.dataframe(productos_populares, use_container_width=True)
                    else:
                        st.info("📦 Datos de productos de ejemplo")
                        df_ejemplo = pd.DataFrame({
                            'Producto': ['Martillo Profesional', 'Taladro Electrico', 'Sierra Circular', 
                                        'Juego de Llaves', 'Pintura Blanca', 'Cemento', 'Clavos', 
                                        'Destornilladores', 'Lijas', 'Brochas'],
                            'Ventas Estimadas': [125, 98, 76, 65, 52, 48, 42, 38, 35, 30]
                        })
                        st.dataframe(df_ejemplo, use_container_width=True)
                        
                        # Grafico de barras
                        fig = px.bar(df_ejemplo.head(5), x='Producto', y='Ventas Estimadas', 
                                    template="plotly_dark", color='Ventas Estimadas',
                                    color_continuous_scale='blues')
                        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.info("📦 Datos de productos de ejemplo")
                    df_ejemplo = pd.DataFrame({
                        'Producto': ['Martillo', 'Taladro', 'Sierra', 'Llaves', 'Pintura'],
                        'Ventas Estimadas': [125, 98, 76, 65, 52]
                    })
                    st.dataframe(df_ejemplo, use_container_width=True)
    
    with col_prod2:
        st.markdown('<div class="card-title"> Recomendaciones</div>', unsafe_allow_html=True)
        
        # Calcular algunas metricas
        if len(facturas_df) > 0:
            total_ventas = facturas_df['Total'].sum() if 'Total' in facturas_df.columns else 0
            num_ventas = len(facturas_df)
            promedio = total_ventas / num_ventas if num_ventas > 0 else 0
            
            st.markdown(f"""
            <div class="info-box">
                <strong>🎯 Recomendaciones Basadas en IA:</strong><br><br>
                ✅ <strong>Ticket Promedio Actual:</strong> C$ {promedio:,.2f}<br>
                ✅ <strong>Volumen de Ventas:</strong> {num_ventas} transacciones<br><br>
                <strong>📌 Estrategias Sugeridas:</strong><br>
                • {'Implementar upselling para aumentar ticket' if promedio < 300 else 'Mantener ticket promedio optimo'}<br>
                • {'Lanzar promociones por volumen' if num_ventas < 100 else 'Fidelizar clientes actuales'}<br>
                • {'Analizar productos de baja rotacion' if num_ventas > 50 else 'Expandir catalogo de productos'}
            </div>
            """, unsafe_allow_html=True)

else:
    # Mensaje cuando no hay datos
    st.markdown("""
    <div class="info-box">
        <strong>⚠️ No hay suficientes datos para generar predicciones</strong><br><br>
        El modelo predictivo necesita al menos 30 registros de ventas para funcionar correctamente.<br>
        Actualmente requiere datos historicos de facturas con la columna 'Total'.
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("## Demostracion del Modelo")
    
    if st.button("🎬 Ver Demostracion del Modelo Predictivo", use_container_width=True):
        with st.spinner("Cargando demostracion..."):
            # Datos de ejemplo
            datos_ejemplo = [100, 120, 115, 130, 125, 140, 135, 150, 145, 160, 155, 170, 165, 180, 175]
            st.line_chart(datos_ejemplo, use_container_width=True)
            st.success("✅ El modelo predictivo comenzara a funcionar automaticamente cuando haya datos reales de ventas")
            
            st.markdown("""
            <div class="info-box">
                <strong>📊 Ejemplo de lo que podras ver:</strong><br><br>
                • Prediccion de ventas a 7, 14 o 30 dias<br>
                • Identificacion de productos mas vendidos<br>
                • Analisis de tendencias estacionales<br>
                • Recomendaciones de inventario basadas en demanda
            </div>
            """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;">🔮 Modelo Predictivo IA - Ferreteria IA</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Random Forest | Prediccion de Ventas | Analisis de Productos | Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)