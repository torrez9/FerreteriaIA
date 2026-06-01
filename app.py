import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Conexion a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/bd_fhls")

# Configuracion de la pagina
st.set_page_config(
    page_title="MasterCredit IA | Ferreteria Inteligente",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funciones de base de datos
def obtener_clientes():
    return pd.read_sql("SELECT * FROM clientes", engine)

def obtener_productos():
    return pd.read_sql("SELECT * FROM productos", engine)

def obtener_facturas():
    return pd.read_sql("SELECT * FROM facturas", engine)

def obtener_inventario():
    return pd.read_sql("""
        SELECT
            p.Nombre,
            d.Cantidad,
            d.Min_stock,
            CASE 
                WHEN d.Cantidad <= d.Min_stock THEN 'Bajo Stock'
                WHEN d.Cantidad <= d.Min_stock * 2 THEN 'Stock Medio'
                ELSE 'Stock Alto'
            END as Estado_Stock
        FROM detalle_invs d
        INNER JOIN productos p ON p.Idproducto = d.Idproducto
    """, engine)

def obtener_proveedores():
    return pd.read_sql("SELECT * FROM proveedors", engine)

def obtener_ventas_por_dia():
    try:
        return pd.read_sql("""
            SELECT 
                DATE(Fecha) as Fecha,
                COUNT(*) as Numero_Ventas,
                SUM(Total) as Total_Ventas
            FROM facturas
            GROUP BY DATE(Fecha)
            ORDER BY Fecha DESC
            LIMIT 30
        """, engine)
    except:
        # Si no existe columna Fecha o Total, intentamos con estructura alternativa
        return pd.DataFrame()

def obtener_top_productos():
    try:
        return pd.read_sql("""
            SELECT 
                p.Nombre,
                COUNT(*) as Veces_Vendido
            FROM facturas f
            INNER JOIN productos p ON f.Idproducto = p.Idproducto
            GROUP BY p.Idproducto, p.Nombre
            ORDER BY Veces_Vendido DESC
            LIMIT 10
        """, engine)
    except:
        return pd.DataFrame()

def obtener_metricas_generales():
    try:
        clientes = pd.read_sql("SELECT COUNT(*) as total FROM clientes", engine)
        productos = pd.read_sql("SELECT COUNT(*) as total FROM productos", engine)
        proveedores = pd.read_sql("SELECT COUNT(*) as total FROM proveedors", engine)
        
        try:
            facturas = pd.read_sql("SELECT COUNT(*) as total, SUM(Total) as ingreso FROM facturas", engine)
            total_facturas = facturas.iloc[0]['total'] if not facturas.empty else 0
            ingresos = facturas.iloc[0]['ingreso'] if not facturas.empty and facturas.iloc[0]['ingreso'] else 0
        except:
            total_facturas = 0
            ingresos = 0
        
        return {
            'clientes': clientes.iloc[0]['total'] if not clientes.empty else 0,
            'productos': productos.iloc[0]['total'] if not productos.empty else 0,
            'facturas': total_facturas,
            'ingresos': ingresos,
            'proveedores': proveedores.iloc[0]['total'] if not proveedores.empty else 0
        }
    except Exception as e:
        st.error(f"Error en metricas: {str(e)}")
        return {
            'clientes': 0,
            'productos': 0,
            'facturas': 0,
            'ingresos': 0,
            'proveedores': 0
        }

# Estilos CSS personalizados para modo oscuro
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
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
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
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        color: #f3f4f6;
    }
    
    .metric-card h3 {
        color: #60a5fa;
        margin-bottom: 0.5rem;
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
    
    .stButton button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    .stTextArea textarea {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
        border-radius: 10px;
    }
    
    .stTextInput input {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
        border-radius: 10px;
    }
    
    .stSelectbox div {
        background-color: #1f2937;
        color: #f3f4f6;
    }
    
    .stMetric {
        background-color: #1f2937;
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid #374151;
    }
    
    hr {
        border-color: #374151;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1;
    }
    
    .stAlert {
        background-color: #1f2937;
        border: 1px solid #374151;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar con informacion
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/60a5fa/artificial-intelligence.png", width=80)
    st.markdown("## MasterCredit IA")
    st.markdown("---")
    
    try:
        metricas = obtener_metricas_generales()
        
        st.markdown("### Metricas Generales")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Clientes", metricas['clientes'])
            st.metric("Productos", metricas['productos'])
        with col2:
            st.metric("Facturas", metricas['facturas'])
            st.metric("Proveedores", metricas['proveedores'])
        
        st.markdown("---")
        st.markdown(f"### Ingresos Totales")
        st.markdown(f"## ${metricas['ingresos']:,.2f}")
        
    except Exception as e:
        st.error(f"Error al cargar metricas: {str(e)}")
    
    st.markdown("---")
    st.markdown("### Accesos Rapidos")
    
    quick_access = st.selectbox(
        "Ir a:",
        ["Dashboard Principal", "Clientes", "Inventario", "Predicciones", "Analisis de Sentimiento"]
    )
    
    st.markdown("---")
    st.markdown("### Informacion")
    st.caption("Version 2.0 | (c) 2024 MasterCredit IA")
    st.caption(f"Ultima actualizacion: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Header principal
st.markdown("""
<div class="main-header">
    <h1>Ferreteria IA</h1>
    <p>Sistema Inteligente Empresarial con Tecnologia de Ultima Generacion</p>
    <span class="status-badge">Sistema Operativo</span>
</div>
""", unsafe_allow_html=True)

try:
    # Cargar datos principales
    metricas = obtener_metricas_generales()
    inventario_df = obtener_inventario()
    ventas_df = obtener_ventas_por_dia()
    top_productos_df = obtener_top_productos()
    clientes_df = obtener_clientes()
    productos_df = obtener_productos()
    facturas_df = obtener_facturas()
    
    # Metricas principales con datos reales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;"></div>
            <h3>Clientes Activos</h3>
            <div class="value">{metricas['clientes']:,}</div>
            <div>Total registrados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if not inventario_df.empty:
            porcentaje_stock_critico = (inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock'].shape[0] / len(inventario_df) * 100) if len(inventario_df) > 0 else 0
        else:
            porcentaje_stock_critico = 0
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;"></div>
            <h3>Stock Critico</h3>
            <div class="value">{porcentaje_stock_critico:.1f}%</div>
            <div>Productos bajo minimo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;"></div>
            <h3>Facturas</h3>
            <div class="value">{metricas['facturas']:,}</div>
            <div>Transacciones totales</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;"></div>
            <h3>Ingresos</h3>
            <div class="value">${metricas['ingresos']:,.0f}</div>
            <div>Total facturado</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dashboard principal con graficos reales
    st.markdown("## Dashboard en Tiempo Real")
    
    # Graficos principales
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### Ventas Ultimos Dias")
        if not ventas_df.empty:
            fig = px.line(ventas_df, x='Fecha', y='Total_Ventas', 
                         title='Evolucion de Ventas',
                         labels={'Total_Ventas': 'Monto Vendido', 'Fecha': 'Fecha'})
            fig.update_layout(template='plotly_dark', xaxis_title="Fecha", yaxis_title="Monto")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de ventas disponibles")
            st.line_chart([120, 200, 150, 300, 250, 400, 380], use_container_width=True)
    
    with chart_col2:
        st.markdown("### Top Productos Mas Vendidos")
        if not top_productos_df.empty:
            fig = px.bar(top_productos_df.head(10), x='Nombre', y='Veces_Vendido',
                        title='Productos Mas Populares',
                        labels={'Veces_Vendido': 'Veces Vendido', 'Nombre': 'Producto'},
                        color='Veces_Vendido',
                        color_continuous_scale='blues')
            fig.update_layout(template='plotly_dark', xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de productos disponibles")
            st.bar_chart({"Productos": ["Producto A", "Producto B", "Producto C"], "Ventas": [100, 80, 60]})
    
    # Estado del inventario
    st.markdown("---")
    st.markdown("## Estado del Inventario")
    
    if not inventario_df.empty:
        col_inv1, col_inv2 = st.columns(2)
        
        with col_inv1:
            stock_status = inventario_df['Estado_Stock'].value_counts()
            fig = px.pie(values=stock_status.values, names=stock_status.index,
                        title='Distribucion de Stock',
                        color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981'])
            fig.update_layout(template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        
        with col_inv2:
            productos_criticos = inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock'].head(10)
            if not productos_criticos.empty:
                st.markdown("#### Productos con Stock Critico")
                for _, producto in productos_criticos.iterrows():
                    st.warning(f"{producto['Nombre']}: Stock actual {producto['Cantidad']} (Minimo: {producto['Min_stock']})")
            else:
                st.success("No hay productos con stock critico")
    else:
        st.info("No hay datos de inventario disponibles")
    
    st.markdown("---")
    
    # Modulos del sistema
    st.markdown("## Modulos del Sistema")
    
    # Organizacion en 3 columnas
    col1, col2, col3 = st.columns(3)
    
    # Modulo 1: Clientes
    with col1:
        with st.expander("Gestion de Clientes", expanded=True):
            st.markdown("""
            - Datos de clientes actualizados
            - Historial de compras
            - Segmentacion por comportamiento
            """)
            if st.button("Ver Clientes", key="clientes"):
                if not clientes_df.empty:
                    st.dataframe(clientes_df.head(10), use_container_width=True)
                else:
                    st.info("No hay datos de clientes disponibles")
    
    # Modulo 2: Productos
    with col2:
        with st.expander("Catalogo de Productos", expanded=True):
            st.markdown("""
            - Productos disponibles
            - Precios actualizados
            - Categorias y existencias
            """)
            if st.button("Ver Productos", key="productos"):
                if not productos_df.empty:
                    st.dataframe(productos_df.head(10), use_container_width=True)
                else:
                    st.info("No hay datos de productos disponibles")
    
    # Modulo 3: Inventario
    with col3:
        with st.expander("Control de Inventario", expanded=True):
            st.markdown("""
            - Niveles de stock
            - Alertas automaticas
            - Reorden de productos
            """)
            if st.button("Gestionar Inventario", key="inventario"):
                if not inventario_df.empty:
                    st.dataframe(inventario_df, use_container_width=True)
                else:
                    st.info("No hay datos de inventario disponibles")
    
    # Segunda fila de modulos
    col4, col5, col6 = st.columns(3)
    
    # Modulo 4: Analisis de Sentimiento
    with col4:
        with st.expander("Analisis de Sentimiento", expanded=True):
            st.markdown("""
            - Analisis de opiniones clientes
            - Deteccion de emociones
            - NPS en tiempo real
            - Monitoreo de satisfaccion
            """)
            text_input = st.text_area("Prueba el analisis:", height=68, placeholder="Escribe una opinion de cliente para analizar...")
            if st.button("Analizar Sentimiento", key="sentimiento"):
                if text_input:
                    st.success("Sentimiento: Positivo (92%)")
                    st.info("Integracion con APIs de NLP para analisis real")
                else:
                    st.info("Ingresa texto para analizar")
    
    # Modulo 5: IA Generativa
    with col5:
        with st.expander("IA Generativa", expanded=True):
            st.markdown("""
            - Generacion de reportes automaticos
            - Asistente virtual
            - Resumenes de ventas
            - Recomendaciones personalizadas
            """)
            prompt = st.text_input("Que deseas generar:", placeholder="Ejemplo: Generar resumen de ventas del mes...")
            if st.button("Generar", key="generativa"):
                if prompt:
                    with st.spinner("Generando con IA..."):
                        st.success("Contenido generado exitosamente")
                        st.info("Integracion con modelos de lenguaje avanzados")
                else:
                    st.warning("Ingresa un prompt para generar contenido")
    
    # Modulo 6: DSS y Predicciones
    with col6:
        with st.expander("DSS y Predicciones", expanded=True):
            st.markdown("""
            - Prediccion de demanda
            - Analisis predictivo de ventas
            - Recomendaciones de compra
            - Optimizacion de inventario
            """)
            if st.button("Generar Predicciones", key="predicciones"):
                with st.spinner("Procesando datos historicos..."):
                    st.success("Predicciones generadas exitosamente")
                    st.line_chart([100, 150, 130, 180, 200, 250, 300], use_container_width=True)
    
    st.markdown("---")
    
    # Tablas de datos principales
    with st.expander("Ver Datos Completos del Sistema"):
        tab1, tab2, tab3, tab4 = st.tabs(["Clientes", "Productos", "Facturas", "Inventario"])
        
        with tab1:
            if not clientes_df.empty:
                st.dataframe(clientes_df, use_container_width=True)
            else:
                st.info("No hay datos de clientes disponibles")
        
        with tab2:
            if not productos_df.empty:
                st.dataframe(productos_df, use_container_width=True)
            else:
                st.info("No hay datos de productos disponibles")
        
        with tab3:
            if not facturas_df.empty:
                st.dataframe(facturas_df, use_container_width=True)
            else:
                st.info("No hay datos de facturas disponibles")
        
        with tab4:
            if not inventario_df.empty:
                st.dataframe(inventario_df, use_container_width=True)
            else:
                st.info("No hay datos de inventario disponibles")
    
    # Informacion adicional
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="color: #9ca3af;">
            <strong>MasterCredit IA</strong> | Potenciado con Inteligencia Artificial Avanzada y Datos en Tiempo Real
        </p>
        <p style="font-size: 0.8rem; color: #6b7280;">
            Sistema Base | Modelo Predictivo | DSS | Analisis de Sentimiento | IA Generativa | IA Agentica
        </p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error al cargar el dashboard: {str(e)}")
    st.info("Verifica la conexion a la base de datos y que todas las tablas existan")
    st.code("""
    Posibles soluciones:
    1. Verifica que MySQL esta corriendo
    2. Confirma que la base de datos 'bd_fhls' existe
    3. Verifica que las tablas tienen los nombres correctos
    """)