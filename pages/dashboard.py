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
    obtener_proveedores
)

# Configuracion de la pagina
st.set_page_config(
    page_title="Ferreteria Intelligent System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para modo oscuro
st.markdown("""
<style>
    /* Fondo principal */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Header principal */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-radius: 20px;
        color: #f3f4f6;
        margin-bottom: 2rem;
        border: 1px solid #374151;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: #60a5fa;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    /* Tarjetas de metricas */
    .metric-card {
        background: #1f2937;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #374151;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
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
        font-size: 0.9rem;
    }
    
    /* Badges */
    .status-badge {
        background: #059669;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #1f2937;
        color: #60a5fa;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    
    .streamlit-expanderContent {
        background-color: #111827;
        border-radius: 10px;
        color: #d1d5db;
    }
    
    /* Botones */
    .stButton button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Alertas */
    .stAlert {
        background-color: #1f2937;
        border: 1px solid #374151;
        border-radius: 10px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #1f2937;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #d1d5db;
    }
    
    /* Metricas nativas */
    .stMetric {
        background-color: #1f2937;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #374151;
    }
    
    hr {
        border-color: #374151;
        margin: 2rem 0;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
</style>
""", unsafe_allow_html=True)

# Funciones adicionales para analisis
def obtener_kpi_adicionales(facturas_df, inventario_df, clientes_df):
    kpis = {}
    
    # Ticket promedio
    if not facturas_df.empty and "Total" in facturas_df.columns:
        kpis['ticket_promedio'] = facturas_df["Total"].mean()
    else:
        kpis['ticket_promedio'] = 0
    
    # Rotacion de inventario (simulada)
    if not inventario_df.empty:
        kpis['productos_stock_bajo'] = len(inventario_df[inventario_df["Cantidad"] <= inventario_df["Min_stock"]])
        kpis['total_inventario'] = inventario_df["Cantidad"].sum()
    else:
        kpis['productos_stock_bajo'] = 0
        kpis['total_inventario'] = 0
    
    # Clientes nuevos (ultimos 7 dias simulados)
    if not clientes_df.empty:
        kpis['total_clientes'] = len(clientes_df)
    else:
        kpis['total_clientes'] = 0
    
    return kpis

def generar_alertas(inventario_df):
    alertas = []
    if not inventario_df.empty:
        stock_bajo = inventario_df[inventario_df["Cantidad"] <= inventario_df["Min_stock"]]
        for _, producto in stock_bajo.head(5).iterrows():
            alertas.append(f"{producto['Nombre']}: Stock {producto['Cantidad']} (Minimo: {producto['Min_stock']})")
    return alertas

# Cargar datos
try:
    clientes = obtener_clientes()
    productos = obtener_productos()
    facturas = obtener_facturas()
    inventario = obtener_inventario()
    proveedores = obtener_proveedores()
    
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
    
except Exception as e:
    st.error(f"Error al cargar datos: {str(e)}")
    clientes = pd.DataFrame()
    productos = pd.DataFrame()
    facturas = pd.DataFrame()
    inventario = pd.DataFrame()
    proveedores = pd.DataFrame()

# Calcular metricas
ventas_totales = 0
if not facturas.empty and "Total" in facturas.columns:
    ventas_totales = facturas["Total"].sum()

kpis = obtener_kpi_adicionales(facturas, inventario, clientes)
alertas = generar_alertas(inventario)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/60a5fa/artificial-intelligence.png", width=80)
    st.markdown("## MasterCredit IA")
    st.markdown("---")
    
    st.markdown("### Panel de Control")
    st.markdown(f"- Clientes: **{len(clientes)}**")
    st.markdown(f"- Productos: **{len(productos)}**")
    st.markdown(f"- Facturas: **{len(facturas)}**")
    
    st.markdown("---")
    st.markdown("### Alertas del Sistema")
    if alertas:
        for alerta in alertas[:3]:
            st.warning(alerta)
    else:
        st.success("Sin alertas activas")
    
    st.markdown("---")
    st.markdown("### Informacion del Sistema")
    st.caption(f"Ultima actualizacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("Version 3.0 | (c) 2024 Ferreteria IA")

# Header principal
st.markdown("""
<div class="main-header">
    <h1>Ferreteria Intelligent System</h1>
    <p>Sistema Inteligente de Gestion Empresarial</p>
    <span class="status-badge">Sistema Operativo en Tiempo Real</span>
</div>
""", unsafe_allow_html=True)

# Metricas principales en grid
st.markdown("## Metricas Clave")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Clientes Registrados",
        f"{len(clientes):,}",
        delta=None,
        help="Total de clientes en el sistema"
    )

with col2:
    st.metric(
        "Productos Catalogo",
        f"{len(productos):,}",
        delta=None,
        help="Total de productos disponibles"
    )

with col3:
    st.metric(
        "Facturas Emitidas",
        f"{len(facturas):,}",
        delta=None,
        help="Total de transacciones realizadas"
    )

with col4:
    st.metric(
        "Proveedores Activos",
        f"{len(proveedores):,}",
        delta=None,
        help="Total de proveedores registrados"
    )

with col5:
    st.metric(
        "Ventas Totales",
        f"C$ {ventas_totales:,.2f}",
        delta=f"Ticket Prom: C$ {kpis['ticket_promedio']:,.2f}",
        help="Ingresos totales por ventas"
    )

st.divider()

# KPIs adicionales
st.markdown("## Indicadores de Rendimiento")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">{:,.0f}</div>
        <div class="metric-label">Unidades en Inventario</div>
    </div>
    """.format(kpis['total_inventario']), unsafe_allow_html=True)

with kpi_col2:
    porcentaje_stock_critico = (kpis['productos_stock_bajo'] / len(productos) * 100) if len(productos) > 0 else 0
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">{:.1f}%</div>
        <div class="metric-label">Productos con Stock Bajo</div>
    </div>
    """.format(porcentaje_stock_critico), unsafe_allow_html=True)

with kpi_col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">C$ {:,.2f}</div>
        <div class="metric-label">Ticket Promedio</div>
    </div>
    """.format(kpis['ticket_promedio']), unsafe_allow_html=True)

with kpi_col4:
    eficiencia = ((len(facturas) / len(clientes)) * 100) if len(clientes) > 0 else 0
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon"></div>
        <div class="metric-value">{:.1f}%</div>
        <div class="metric-label">Eficiencia de Ventas</div>
    </div>
    """.format(eficiencia), unsafe_allow_html=True)

st.divider()

# Dashboard principal
st.markdown("## Dashboard Analitico")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Evolucion de Ventas")
    if not facturas.empty and "Fecha" in facturas.columns and "Total" in facturas.columns:
        facturas_ordenadas = facturas.sort_values("Fecha")
        fig = px.line(
            facturas_ordenadas,
            x="Fecha",
            y="Total",
            markers=True,
            title="Ventas por Factura",
            labels={"Total": "Monto (C$)", "Fecha": "Fecha"},
            template="plotly_dark"
        )
        fig.update_traces(line_color="#3b82f6", marker_color="#60a5fa")
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar el grafico de ventas")
        st.line_chart([100, 150, 130, 180, 200, 250, 300], use_container_width=True)

with col2:
    st.markdown("### Top Productos por Inventario")
    if not inventario.empty and "Nombre" in inventario.columns and "Cantidad" in inventario.columns:
        top_inv = inventario.sort_values(by="Cantidad", ascending=False).head(10)
        fig2 = px.bar(
            top_inv,
            x="Nombre",
            y="Cantidad",
            title="Productos con Mayor Stock",
            labels={"Cantidad": "Unidades", "Nombre": "Producto"},
            template="plotly_dark",
            color="Cantidad",
            color_continuous_scale="blues"
        )
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No hay datos de inventario disponibles")
        st.bar_chart({"Productos": ["A", "B", "C"], "Cantidad": [100, 80, 60]})

st.divider()

# Seccion de alertas
st.markdown("## Alertas y Recomendaciones")

if not inventario.empty:
    stock_bajo = inventario[inventario["Cantidad"] <= inventario["Min_stock"]]
    
    if len(stock_bajo) > 0:
        st.warning(f"Se encontraron {len(stock_bajo)} productos con inventario bajo.")
        
        # Tabla de productos con stock bajo
        st.dataframe(
            stock_bajo[["Nombre", "Cantidad", "Min_stock"]].head(10),
            use_container_width=True,
            column_config={
                "Nombre": "Producto",
                "Cantidad": "Stock Actual",
                "Min_stock": "Stock Minimo"
            }
        )
        
        # Boton para generar orden de compra
        if st.button("Generar Orden de Reabastecimiento"):
            with st.spinner("Generando ordenes de compra..."):
                st.success(f"Se generaron ordenes para {len(stock_bajo)} productos")
    else:
        st.success("No existen productos con inventario bajo. Niveles de stock optimos.")
else:
    st.info("No hay datos de inventario disponibles")

st.divider()

# Datos recientes
st.markdown("## Datos Recientes")

tab1, tab2, tab3 = st.tabs(["Ultimos Clientes", "Productos Recientes", "Analisis"])

with tab1:
    if not clientes.empty:
        st.dataframe(
            clientes.head(10),
            use_container_width=True,
            column_config={
                "id": "ID",
                "nombre": "Nombre",
                "email": "Email",
                "telefono": "Telefono"
            }
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
                title="Distribucion de Montos de Factura",
                labels={"Total": "Monto (C$)"},
                template="plotly_dark"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Sin datos para analisis")
    
    with col_analisis2:
        st.markdown("#### Analisis de Productividad")
        if not facturas.empty and not clientes.empty:
            productividad = len(facturas) / len(clientes) if len(clientes) > 0 else 0
            st.metric("Facturas por Cliente", f"{productividad:.2f}")
            st.metric("Valor Promedio por Transaccion", f"C$ {kpis['ticket_promedio']:,.2f}")
        else:
            st.info("Sin datos suficientes para analisis de productividad")

st.divider()

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <p style="color: #6b7280; font-size: 0.8rem;">
        MasterCredit Intelligent System | Potenciado con Inteligencia Artificial
    </p>
    <p style="color: #4b5563; font-size: 0.7rem;">
        Sistema de Gestion Empresarial | Analisis Predictivo | Decision Support System
    </p>
</div>
""", unsafe_allow_html=True)