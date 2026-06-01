import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from database.models import (
    obtener_clientes,
    obtener_productos,
    obtener_facturas,
    obtener_inventario,
    obtener_proveedores,
    obtener_ventas_por_dia
)
from ml.predictor import predictor

# Configuracion de la pagina
st.set_page_config(
    page_title="Ferreteria IA - Sistema Inteligente",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS UNIFICADOS MODO OSCURO ====================
st.markdown("""
<style>
    /* === ESTILOS BASE === */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* === SIDEBAR ELEGANTE === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    /* Logo y titulo del sidebar */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 1rem;
        border-bottom: 1px solid rgba(96, 165, 250, 0.2);
        margin-bottom: 1rem;
    }
    
    .sidebar-logo {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sidebar-subtitle {
        font-size: 0.7rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Menu items elegantes */
    .menu-section {
        margin: 1rem 0 0.5rem 0;
        padding: 0 0.5rem;
    }
    
    .menu-section-title {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #6b7280;
        padding: 0.5rem 0.75rem;
        margin-top: 0.5rem;
    }
    
    /* Botones personalizados tipo menu */
    .custom-menu-btn {
        background: transparent;
        border: none;
        width: 100%;
        text-align: left;
        padding: 0.6rem 0.75rem;
        margin: 0.2rem 0;
        border-radius: 10px;
        color: #cbd5e1;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .custom-menu-btn:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #60a5fa;
        transform: translateX(5px);
    }
    
    .custom-menu-btn.active {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    /* Separador */
    .menu-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.3), transparent);
        margin: 0.75rem 0.5rem;
    }
    
    /* Estado del sistema en sidebar */
    .system-status {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 0.75rem;
        margin-top: 1rem;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    /* === TARJETAS ESTANDAR === */
    .card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3f 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(96, 165, 250, 0.2);
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
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
    
    .card-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #fbbf24;
        margin: 0.5rem 0;
    }
    
    .card-label {
        font-size: 0.85rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
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
    
    /* === BADGE === */
    .badge {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: 0.3rem 1.2rem;
        border-radius: 30px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* === BOTONES ESTANDAR === */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
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
    
    /* === DATAFRAMES === */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* === METRICAS === */
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
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #d1d5db;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    /* === ALERTAS === */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    /* === DIVIDERS === */
    hr {
        border-color: rgba(96, 165, 250, 0.2);
        margin: 1.5rem 0;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 16px;
        margin-top: 2rem;
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
    
    ::-webkit-scrollbar-thumb:hover {
        background: #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES AUXILIARES ====================

def render_sidebar():
    """Renderiza el sidebar elegante"""
    
    # Header del sidebar
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo"></div>
        <div class="sidebar-title">Ferreteria IA</div>
        <div class="sidebar-subtitle">Sistema Inteligente Empresarial</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu Dashboard
    st.markdown('<div class="menu-section-title">PRINCIPAL</div>', unsafe_allow_html=True)
    if st.button(" Dashboard", use_container_width=True, key="menu_dashboard"):
        st.switch_page("app.py")
    
    st.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)
    
    # Modulos del Sistema
    st.markdown('<div class="menu-section-title">MODULOS DEL SISTEMA</div>', unsafe_allow_html=True)
    
    if st.button(" Clientes", use_container_width=True, key="menu_clientes"):
        st.switch_page("pages/clientes.py")
    
    if st.button(" Productos", use_container_width=True, key="menu_productos"):
        st.switch_page("pages/productos.py")
    
    if st.button(" Inventario", use_container_width=True, key="menu_inventario"):
        st.switch_page("pages/inventario.py")
    
    st.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)
    
    # Componentes IA
    st.markdown('<div class="menu-section-title">INTELIGENCIA ARTIFICIAL</div>', unsafe_allow_html=True)
    
    if st.button(" Predicciones IA", use_container_width=True, key="menu_predicciones"):
        st.switch_page("pages/predicciones.py")
    
    if st.button(" DSS - Decisiones", use_container_width=True, key="menu_dss"):
        st.switch_page("pages/dss.py")
    
    if st.button(" Analisis Sentimiento", use_container_width=True, key="menu_sentimiento"):
        st.switch_page("pages/sentimientos.py")
    
    if st.button(" IA Generativa", use_container_width=True, key="menu_generativa"):
        st.switch_page("pages/ia_generativa.py")
    
    if st.button(" IA Agentica", use_container_width=True, key="menu_agentica"):
        st.switch_page("pages/agente.py")
    
    st.markdown('<div class="menu-divider"></div>', unsafe_allow_html=True)
    
    # Estado del sistema
    st.markdown("""
    <div class="system-status">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #9ca3af;">Sistema</span>
            <span style="color: #10b981;"> Activo</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #9ca3af;">IA</span>
            <span style="color: #10b981;"> Online</span>
        </div>
        <div style="margin-top: 0.75rem; font-size: 0.7rem; color: #6b7280; text-align: center;">
            {0}
        </div>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)

def mostrar_tarjeta_ia(titulo, descripciones, boton_texto, pagina):
    """Muestra una tarjeta para componentes IA estandarizada"""
    with st.container():
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{titulo}</div>
        </div>
        """, unsafe_allow_html=True)
        for desc in descripciones:
            st.markdown(f"- {desc}")
        if st.button(boton_texto, key=f"btn_{pagina}", use_container_width=True):
            st.switch_page(pagina)

# ==================== CARGA DE DATOS ====================
clientes_df = obtener_clientes()
productos_df = obtener_productos()
facturas_df = obtener_facturas()
inventario_df = obtener_inventario()
proveedores_df = obtener_proveedores()
ventas_df = obtener_ventas_por_dia()

# ==================== RENDER SIDEBAR ====================
with st.sidebar:
    render_sidebar()

# ==================== HEADER PRINCIPAL ====================
st.markdown("""
<div class="main-header">
    <h1>Ferreteria IA</h1>
    <p>Sistema Inteligente Empresarial con 6 Componentes de IA</p>
    <span class="badge">Todos los Modulos Activos</span>
</div>
""", unsafe_allow_html=True)

# ==================== METRICAS PRINCIPALES ====================
st.markdown("### Metricas Clave")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Clientes", f"{len(clientes_df):,}")
with col2:
    st.metric("Productos", f"{len(productos_df):,}")
with col3:
    st.metric("Facturas", f"{len(facturas_df):,}")
with col4:
    st.metric("Proveedores", f"{len(proveedores_df):,}")

st.divider()

# ==================== DASHBOARD GRAFICOS ====================
st.markdown("### Dashboard Analitico")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown('<div class="card-title">Evolucion de Ventas</div>', unsafe_allow_html=True)
    if not ventas_df.empty:
        fig = px.line(
            ventas_df, 
            x='Fecha', 
            y='Total_Ventas', 
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Fecha",
            yaxis_title="Ventas (C$)"
        )
        fig.update_traces(line_color="#3b82f6")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de ventas disponibles")

with col_graf2:
    st.markdown('<div class="card-title">Distribucion de Stock</div>', unsafe_allow_html=True)
    if not inventario_df.empty and 'Estado_Stock' in inventario_df.columns:
        estado_counts = inventario_df['Estado_Stock'].value_counts()
        fig = px.pie(
            values=estado_counts.values, 
            names=estado_counts.index,
            template="plotly_dark",
            color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981']
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de inventario disponibles")

st.divider()

# ==================== COMPONENTES IA ====================
st.markdown("### Componentes de Inteligencia Artificial")

col_ia1, col_ia2, col_ia3 = st.columns(3)

with col_ia1:
    mostrar_tarjeta_ia(
        " Modelo Predictivo",
        ["Prediccion de ventas", "Productos populares", "Tendencias de mercado"],
        "Ver Predicciones",
        "pages/predicciones.py"
    )

with col_ia2:
    mostrar_tarjeta_ia(
        " DSS - Decisiones",
        ["Alertas automaticas", "Recomendaciones", "Analisis de descuentos"],
        "Ver DSS",
        "pages/dss.py"
    )

with col_ia3:
    mostrar_tarjeta_ia(
        " IA Agentica",
        ["Monitoreo autonomo", "Procesamiento automatico", "Cadena suministro"],
        "Ver Agente IA",
        "pages/agente.py"
    )

col_ia4, col_ia5, col_ia6 = st.columns(3)

with col_ia4:
    mostrar_tarjeta_ia(
        " Analisis Sentimiento",
        ["Opiniones de clientes", "Clasificacion emocional", "Feedback automatico"],
        "Ver Sentimiento",
        "pages/sentimientos.py"
    )

with col_ia5:
    mostrar_tarjeta_ia(
        " IA Generativa",
        ["Reportes automaticos", "Resumenes de ventas", "Correos promocionales"],
        "Ver IA Generativa",
        "pages/ia_generativa.py"
    )

with col_ia6:
    mostrar_tarjeta_ia(
        " Sistema Base",
        ["Gestion de clientes", "Catalogo productos", "Control inventario"],
        "Ver Sistema",
        "pages/clientes.py"
    )

st.divider()

# ==================== ALERTAS DE INVENTARIO ====================
st.markdown("### Alertas del Sistema")

if not inventario_df.empty and 'Estado_Stock' in inventario_df.columns:
    productos_bajos = inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock']
    
    if not productos_bajos.empty:
        st.warning(f"Se encontraron {len(productos_bajos)} productos con stock bajo")
        st.dataframe(
            productos_bajos[['Nombre', 'Cantidad', 'Min_stock']].head(10),
            use_container_width=True,
            column_config={
                "Nombre": "Producto",
                "Cantidad": st.column_config.NumberColumn("Stock Actual", format="%d"),
                "Min_stock": st.column_config.NumberColumn("Stock Minimo", format="%d")
            }
        )
    else:
        st.success("No hay productos con stock critico")
else:
    st.info("No hay datos de inventario disponibles")

st.divider()

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;">Ferreteria IA - Sistema Inteligente Empresarial</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Sistema Base | Modelo Predictivo | DSS | Analisis Sentimiento | IA Generativa | IA Agentica
    </p>
</div>
""", unsafe_allow_html=True)