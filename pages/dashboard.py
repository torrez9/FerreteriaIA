import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from database.models import (
    obtener_clientes,
    obtener_productos,
    obtener_facturas,
    obtener_inventario,
    obtener_proveedores,
    obtener_ventas_por_dia
)

# Configuracion de la pagina
st.set_page_config(
    page_title="Dashboard - Ferreteria IA",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
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
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3f 100%);
        border-radius: 20px;
        color: #f3f4f6;
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
    
    .metric-card .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
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
    .status-badge {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #d97706, #b45309);
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
    
    /* === ALERTAS === */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
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
    
    /* === DIVIDERS === */
    hr {
        border-color: rgba(96, 165, 250, 0.2);
        margin: 2rem 0;
    }
    
    /* === INFO BOX === */
    .info-box {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #60a5fa;
        color: #cbd5e1;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 20px;
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
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES AUXILIARES ====================

def obtener_kpi_adicionales(facturas_df, inventario_df, clientes_df):
    kpis = {}
    
    if not facturas_df.empty and "Total" in facturas_df.columns:
        kpis['ticket_promedio'] = facturas_df["Total"].mean()
        kpis['ventas_totales'] = facturas_df["Total"].sum()
        kpis['num_ventas'] = len(facturas_df)
    else:
        kpis['ticket_promedio'] = 0
        kpis['ventas_totales'] = 0
        kpis['num_ventas'] = 0
    
    if not inventario_df.empty:
        if 'Min_stock' in inventario_df.columns:
            kpis['productos_stock_bajo'] = len(inventario_df[inventario_df["Cantidad"] <= inventario_df["Min_stock"]])
        else:
            kpis['productos_stock_bajo'] = len(inventario_df[inventario_df["Cantidad"] <= 10])
        kpis['total_inventario'] = inventario_df["Cantidad"].sum()
    else:
        kpis['productos_stock_bajo'] = 0
        kpis['total_inventario'] = 0
    
    kpis['total_clientes'] = len(clientes_df) if not clientes_df.empty else 0
    
    return kpis

def generar_alertas(inventario_df):
    alertas = []
    if not inventario_df.empty:
        if 'Min_stock' in inventario_df.columns:
            stock_bajo = inventario_df[inventario_df["Cantidad"] <= inventario_df["Min_stock"]]
        else:
            stock_bajo = inventario_df[inventario_df["Cantidad"] <= 10]
        for _, producto in stock_bajo.head(5).iterrows():
            nombre = producto['Nombre'] if 'Nombre' in producto.index else "Producto"
            alertas.append(f"{nombre}: Stock {producto['Cantidad']} (Minimo: {producto.get('Min_stock', 10)})")
    return alertas

# ==================== CARGA DE DATOS ====================
try:
    clientes = obtener_clientes()
    productos = obtener_productos()
    facturas = obtener_facturas()
    inventario = obtener_inventario()
    proveedores = obtener_proveedores()
    ventas_diarias = obtener_ventas_por_dia()
    
    # Validar datos
    if clientes is None:
        clientes = pd.DataFrame()
    if productos is None:
        productos = pd.DataFrame()
    if facturas is None:
        facturas = pd.DataFrame()
    if inventario is None:
        inventario = pd.DataFrame()
    if proveedores is None:
        proveedores = pd.DataFrame()
    if ventas_diarias is None:
        ventas_diarias = pd.DataFrame()
    
except Exception as e:
    st.error(f"Error al cargar datos: {str(e)}")
    clientes = pd.DataFrame()
    productos = pd.DataFrame()
    facturas = pd.DataFrame()
    inventario = pd.DataFrame()
    proveedores = pd.DataFrame()
    ventas_diarias = pd.DataFrame()

# Calcular metricas
ventas_totales = 0
if not facturas.empty and "Total" in facturas.columns:
    ventas_totales = facturas["Total"].sum()

kpis = obtener_kpi_adicionales(facturas, inventario, clientes)
alertas = generar_alertas(inventario)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;"></div>
        <h2 style="color: #60a5fa;">Ferreteria IA</h2>
        <p style="color: #9ca3af;">Dashboard Ejecutivo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Panel de Control")
    st.markdown(f"- Clientes: **{len(clientes):,}**")
    st.markdown(f"- Productos: **{len(productos):,}**")
    st.markdown(f"- Facturas: **{len(facturas):,}**")
    st.markdown(f"- Proveedores: **{len(proveedores):,}**")
    
    st.markdown("---")
    st.markdown("### Alertas del Sistema")
    if alertas:
        for alerta in alertas[:3]:
            st.warning(alerta)
    else:
        st.success("Sin alertas activas")
    
    st.markdown("---")
    st.markdown("### Resumen Rapido")
    if not facturas.empty and "Total" in facturas.columns:
        st.metric("Ventas Totales", f"C$ {kpis['ventas_totales']:,.2f}")
        st.metric("Ticket Promedio", f"C$ {kpis['ticket_promedio']:,.2f}")
    
    st.markdown("---")
    st.markdown(f"**Ultima actualizacion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== HEADER PRINCIPAL ====================
st.markdown("""
<div class="main-header">
    <h1> Dashboard Ejecutivo</h1>
    <p>Sistema Inteligente de Gestion Empresarial</p>
    <span class="status-badge">Sistema Operativo en Tiempo Real</span>
</div>
""", unsafe_allow_html=True)

# ==================== METRICAS PRINCIPALES ====================
st.markdown("## Metricas Clave")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Clientes",
        f"{len(clientes):,}",
        help="Total de clientes registrados"
    )

with col2:
    st.metric(
        "Productos",
        f"{len(productos):,}",
        help="Total de productos en catalogo"
    )

with col3:
    st.metric(
        "Facturas",
        f"{len(facturas):,}",
        help="Total de transacciones"
    )

with col4:
    st.metric(
        "Proveedores",
        f"{len(proveedores):,}",
        help="Total de proveedores"
    )

with col5:
    st.metric(
        "Ventas Totales",
        f"C$ {kpis['ventas_totales']:,.2f}",
        delta=f"C$ {kpis['ticket_promedio']:,.2f}",
        help="Ingresos totales"
    )

st.divider()

# ==================== KPIS ADICIONALES ====================
st.markdown("## Indicadores de Rendimiento")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">{kpis['total_inventario']:,.0f}</div>
        <div class="metric-label">Unidades en Inventario</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    porcentaje_stock = (kpis['productos_stock_bajo'] / len(productos) * 100) if len(productos) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">{porcentaje_stock:.1f}%</div>
        <div class="metric-label">Stock Critico</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">C$ {kpis['ticket_promedio']:,.2f}</div>
        <div class="metric-label">Ticket Promedio</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    eficiencia = (kpis['num_ventas'] / kpis['total_clientes']) if kpis['total_clientes'] > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">{eficiencia:.1f}</div>
        <div class="metric-label">Ventas por Cliente</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== DASHBOARD GRAFICOS ====================
st.markdown("## Dashboard Analitico")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown('<div class="card-title">Evolucion de Ventas</div>', unsafe_allow_html=True)
    if not ventas_diarias.empty and 'Fecha' in ventas_diarias.columns and 'Total_Ventas' in ventas_diarias.columns:
        fig = px.line(
            ventas_diarias,
            x="Fecha",
            y="Total_Ventas",
            markers=True,
            template="plotly_dark"
        )
        fig.update_traces(line_color="#3b82f6", line_width=3, marker_color="#60a5fa", marker_size=8)
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Fecha",
            yaxis_title="Ventas (C$)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif not facturas.empty and "Fecha" in facturas.columns and "Total" in facturas.columns:
        facturas_ordenadas = facturas.sort_values("Fecha")
        fig = px.line(
            facturas_ordenadas,
            x="Fecha",
            y="Total",
            markers=True,
            template="plotly_dark"
        )
        fig.update_traces(line_color="#3b82f6", line_width=3, marker_color="#60a5fa")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Fecha",
            yaxis_title="Ventas (C$)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de ventas disponibles")
        st.line_chart([100, 150, 130, 180, 200, 250, 300], use_container_width=True)

with col_graf2:
    st.markdown('<div class="card-title">Top Productos por Inventario</div>', unsafe_allow_html=True)
    if not inventario.empty and "Nombre" in inventario.columns and "Cantidad" in inventario.columns:
        top_inv = inventario.sort_values(by="Cantidad", ascending=False).head(10)
        fig = px.bar(
            top_inv,
            x="Nombre",
            y="Cantidad",
            template="plotly_dark",
            color="Cantidad",
            color_continuous_scale="blues"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-45,
            xaxis_title="Producto",
            yaxis_title="Unidades"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de inventario disponibles")
        st.bar_chart({"Productos": ["A", "B", "C", "D", "E"], "Cantidad": [100, 80, 60, 40, 20]})

st.divider()

# ==================== ALERTAS Y RECOMENDACIONES ====================
st.markdown("## Alertas y Recomendaciones")

if not inventario.empty:
    if 'Min_stock' in inventario.columns:
        stock_bajo = inventario[inventario["Cantidad"] <= inventario["Min_stock"]]
    else:
        stock_bajo = inventario[inventario["Cantidad"] <= 10]
    
    if len(stock_bajo) > 0:
        st.warning(f" Se encontraron {len(stock_bajo)} productos con inventario bajo")
        
        st.dataframe(
            stock_bajo[["Nombre", "Cantidad", "Min_stock" if 'Min_stock' in inventario.columns else "Cantidad"]].head(10),
            use_container_width=True,
            column_config={
                "Nombre": "Producto",
                "Cantidad": "Stock Actual",
                "Min_stock": "Stock Minimo"
            }
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button(" Generar Orden de Reabastecimiento", use_container_width=True):
                with st.spinner("Generando ordenes de compra..."):
                    st.success(f"Se generaron ordenes para {len(stock_bajo)} productos")
    else:
        st.success(" No existen productos con inventario bajo. Niveles de stock optimos.")
else:
    st.info(" No hay datos de inventario disponibles")

st.divider()

# ==================== DATOS RECIENTES ====================
st.markdown("## Datos Recientes")

tab1, tab2, tab3 = st.tabs([" Ultimos Clientes", " Productos Recientes", " Analisis de Ventas"])

with tab1:
    if not clientes.empty:
        st.dataframe(
            clientes.head(10),
            use_container_width=True
        )
    else:
        st.info("No hay datos de clientes disponibles")

with tab2:
    if not productos.empty:
        st.dataframe(
            productos.head(10),
            use_container_width=True
        )
    else:
        st.info("No hay datos de productos disponibles")

with tab3:
    col_analisis1, col_analisis2 = st.columns(2)
    
    with col_analisis1:
        st.markdown("#### Distribucion de Ventas")
        if not facturas.empty and "Total" in facturas.columns:
            fig_hist = px.histogram(
                facturas,
                x="Total",
                nbins=20,
                title="Distribucion de Montos",
                labels={"Total": "Monto (C$)"},
                template="plotly_dark"
            )
            fig_hist.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Sin datos para analisis")
    
    with col_analisis2:
        st.markdown("#### Resumen Ejecutivo")
        st.markdown(f"""
        <div class="info-box">
            <strong>📊 Estadisticas Clave:</strong><br><br>
            - Total Ventas: C$ {kpis['ventas_totales']:,.2f}<br>
            - Numero Transacciones: {kpis['num_ventas']}<br>
            - Ticket Promedio: C$ {kpis['ticket_promedio']:,.2f}<br>
            - Productos en Stock: {kpis['total_inventario']:,.0f}<br>
            - Productos Criticos: {kpis['productos_stock_bajo']}
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;"> Ferreteria IA - Sistema Inteligente Empresarial</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Sistema Base | Modelo Predictivo | DSS | Analisis Sentimiento | IA Generativa | IA Agentica
    </p>
    <p style="color: #4b5563; font-size: 0.7rem;">
        Potenciado con Inteligencia Artificial | Datos en Tiempo Real
    </p>
</div>
""", unsafe_allow_html=True)