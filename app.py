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

# Estilos CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-radius: 20px;
        color: #f3f4f6;
        margin-bottom: 2rem;
        border: 1px solid #374151;
    }
    
    .main-header h1 {
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    
    .metric-card {
        background: #1f2937;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #374151;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: bold;
        color: #fbbf24;
    }
    
    .status-badge {
        background: #059669;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        display: inline-block;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* Estilo para los links del sidebar */
    .sidebar-link {
        display: block;
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
        border-radius: 8px;
        color: #cbd5e1;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .sidebar-link:hover {
        background-color: #1e293b;
        color: #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
clientes_df = obtener_clientes()
productos_df = obtener_productos()
facturas_df = obtener_facturas()
inventario_df = obtener_inventario()
proveedores_df = obtener_proveedores()
ventas_df = obtener_ventas_por_dia()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/60a5fa/artificial-intelligence.png", width=80)
    st.markdown("# Ferreteria IA")
    st.markdown("### Sistema Inteligente Empresarial")
    st.markdown("---")
    
    st.markdown("### Navegacion")
    
    # Usando botones en lugar de page_link para evitar errores
    if st.button(" Dashboard Principal", use_container_width=True, key="btn_dash"):
        st.switch_page("app.py")
    
    st.markdown("---")
    st.markdown("#### Modulos del Sistema")
    
    if st.button(" Clientes", use_container_width=True, key="btn_clientes"):
        st.switch_page("pages/clientes.py")
    
    if st.button(" Productos", use_container_width=True, key="btn_productos"):
        st.switch_page("pages/productos.py")
    
    if st.button(" Inventario", use_container_width=True, key="btn_inventario"):
        st.switch_page("pages/inventario.py")
    
    st.markdown("---")
    st.markdown("#### Componentes IA")
    
    if st.button(" Predicciones IA", use_container_width=True, key="btn_pred"):
        st.switch_page("pages/predicciones.py")
    
    if st.button(" DSS - Decisiones", use_container_width=True, key="btn_dss"):
        st.switch_page("pages/dss.py")
    
    if st.button(" Analisis Sentimiento", use_container_width=True, key="btn_sent"):
        st.switch_page("pages/sentimientos.py")
    
    if st.button(" IA Generativa", use_container_width=True, key="btn_gen"):
        st.switch_page("pages/ia_generativa.py")
    
    if st.button(" IA Agentica", use_container_width=True, key="btn_age"):
        st.switch_page("pages/agente.py")
    
    st.markdown("---")
    st.markdown(f"**Ultima actualizacion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M'))

# Header
st.markdown("""
<div class="main-header">
    <h1>Ferreteria IA</h1>
    <p>Sistema Inteligente Empresarial con 6 Componentes de IA</p>
    <span class="status-badge">Todos los Modulos Activos</span>
</div>
""", unsafe_allow_html=True)

# Metricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Clientes", len(clientes_df))
with col2:
    st.metric("Productos", len(productos_df))
with col3:
    st.metric("Facturas", len(facturas_df))
with col4:
    st.metric("Proveedores", len(proveedores_df))

st.divider()

# Dashboard graficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Ventas por Dia")
    if not ventas_df.empty:
        fig = px.line(ventas_df, x='Fecha', y='Total_Ventas', 
                     title="Evolucion de Ventas",
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de ventas")

with col_graf2:
    st.subheader("Estado del Inventario")
    if not inventario_df.empty:
        if 'Estado_Stock' in inventario_df.columns:
            estado_counts = inventario_df['Estado_Stock'].value_counts()
            fig = px.pie(values=estado_counts.values, names=estado_counts.index,
                        title="Distribucion de Stock", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de estado de stock")
    else:
        st.info("No hay datos de inventario")

# Componentes IA destacados
st.divider()
st.subheader("Componentes de IA Disponibles")

col_ia1, col_ia2, col_ia3 = st.columns(3)

with col_ia1:
    st.markdown("""
    ### Modelo Predictivo
    - Prediccion de ventas
    - Productos populares
    - Tendencias de mercado
    """)
    if st.button("Ver Predicciones", key="btn_pred_main"):
        st.switch_page("pages/predicciones.py")

with col_ia2:
    st.markdown("""
    ### DSS - Decisiones
    - Alertas automaticas
    - Recomendaciones
    - Analisis de descuentos
    """)
    if st.button("Ver DSS", key="btn_dss_main"):
        st.switch_page("pages/dss.py")

with col_ia3:
    st.markdown("""
    ### IA Agentica
    - Monitoreo autonomo
    - Procesamiento automatico
    - Cadena suministro
    """)
    if st.button("Ver Agente IA", key="btn_agente_main"):
        st.switch_page("pages/agente.py")

# Segunda fila de componentes IA
st.divider()
col_ia4, col_ia5, col_ia6 = st.columns(3)

with col_ia4:
    st.markdown("""
    ### Analisis de Sentimiento
    - Opiniones de clientes
    - Clasificacion emocional
    - Feedback automatico
    """)
    if st.button("Ver Sentimiento", key="btn_sent_main"):
        st.switch_page("pages/sentimientos.py")

with col_ia5:
    st.markdown("""
    ### IA Generativa
    - Reportes automaticos
    - Resumenes de ventas
    - Correos promocionales
    """)
    if st.button("Ver IA Generativa", key="btn_gen_main"):
        st.switch_page("pages/ia_generativa.py")

with col_ia6:
    st.markdown("""
    ### Sistema Base
    - Gestion de clientes
    - Catalogo productos
    - Control inventario
    """)
    if st.button("Ver Sistema", key="btn_sys_main"):
        st.switch_page("pages/clientes.py")

st.divider()

# Tabla de productos con stock bajo
if not inventario_df.empty and 'Estado_Stock' in inventario_df.columns:
    st.subheader("Alertas de Inventario")
    productos_bajos = inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock']
    
    if not productos_bajos.empty:
        st.warning(f"Se encontraron {len(productos_bajos)} productos con stock bajo")
        st.dataframe(productos_bajos[['Nombre', 'Cantidad', 'Min_stock']].head(10), use_container_width=True)
    else:
        st.success("No hay productos con stock critico")

st.divider()
st.markdown("""
<div style="text-align: center; color: #6b7280;">
    Sistema Base | Modelo Predictivo | DSS | Analisis Sentimiento | IA Generativa | IA Agentica
</div>
""", unsafe_allow_html=True)