import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from database.models import obtener_inventario, obtener_proveedores

# Configuracion de la pagina
st.set_page_config(
    page_title="IA Agentica - Ferreteria IA", 
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
    
    /* === BADGES === */
    .badge-success {
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
    
    /* === INFO BOX === */
    .info-box {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #60a5fa;
        color: #cbd5e1;
    }
    
    /* === STATUS CARD === */
    .status-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    .status-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
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
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1> IA Agentica</h1>
    <p>Agente Inteligente Autonomo - Monitoreo y Ejecucion Automatica</p>
    <span class="badge-success">Sistema Autonomo Activo</span>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
inventario_df = obtener_inventario()
proveedores_df = obtener_proveedores()

# ==================== CLASE AGENTE INTELIGENTE ====================
class AgenteInteligente:
    def __init__(self, inventario, proveedores):
        self.inventario = inventario
        self.proveedores = proveedores
        self.tareas = []
    
    def obtener_nombre_proveedor(self):
        """Obtiene el nombre del proveedor de forma segura"""
        if self.proveedores.empty:
            return "Proveedor Default"
        
        posibles_columnas = ['nombre', 'Nombre', 'NOMBRE', 'nombre_proveedor', 'proveedor', 'Proveedor', 'name', 'Name']
        
        for col in posibles_columnas:
            if col in self.proveedores.columns:
                return str(self.proveedores.iloc[0][col])
        
        return str(self.proveedores.iloc[0].iloc[0]) if len(self.proveedores.columns) > 0 else "Proveedor Default"
    
    def monitorear_stock(self):
        """Monitorea niveles de stock"""
        alertas = []
        if not self.inventario.empty:
            if 'Cantidad' in self.inventario.columns and 'Min_stock' in self.inventario.columns:
                criticos = self.inventario[self.inventario['Cantidad'] <= self.inventario['Min_stock']]
                for idx, prod in criticos.iterrows():
                    nombre_producto = prod['Nombre'] if 'Nombre' in prod.index else f"Producto {idx}"
                    alertas.append({
                        'producto': nombre_producto,
                        'stock_actual': prod['Cantidad'],
                        'minimo': prod['Min_stock']
                    })
            elif 'Cantidad' in self.inventario.columns:
                criticos = self.inventario[self.inventario['Cantidad'] <= 10]
                for idx, prod in criticos.iterrows():
                    nombre_producto = prod['Nombre'] if 'Nombre' in prod.index else f"Producto {idx}"
                    alertas.append({
                        'producto': nombre_producto,
                        'stock_actual': prod['Cantidad'],
                        'minimo': 10
                    })
        return alertas
    
    def procesar_pedido(self, producto, cantidad):
        """Procesa pedido automaticamente"""
        pedido = {
            'producto': producto,
            'cantidad': cantidad,
            'proveedor': self.obtener_nombre_proveedor(),
            'fecha': datetime.now(),
            'estado': 'Procesado por Agente IA',
            'numero_orden': f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        self.tareas.append(pedido)
        return pedido
    
    def ejecutar(self):
        """Ejecuta el ciclo del agente"""
        alertas = self.monitorear_stock()
        resultados = []
        
        for alerta in alertas[:5]:
            cantidad_pedido = alerta['minimo'] * 2
            pedido = self.procesar_pedido(alerta['producto'], cantidad_pedido)
            resultados.append(pedido)
        
        return {
            'alertas': len(alertas),
            'pedidos': len(resultados),
            'detalles': resultados
        }

# ==================== CREAR INSTANCIA DEL AGENTE ====================
agente = AgenteInteligente(inventario_df, proveedores_df)

# ==================== SIDEBAR DE ESTADO ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">🤖</div>
        <h2 style="color: #60a5fa;">Agente IA</h2>
        <p style="color: #9ca3af;">Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Estado del Agente")
    st.markdown("""
    <div class="status-card">
        <div class="status-icon">🟢</div>
        <div style="font-size: 1.2rem; font-weight: bold;">Agente Activo</div>
        <div style="color: #9ca3af; font-size: 0.8rem;">Monitoreo 24/7</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Capacidades")
    st.markdown("""
    - 📊 Monitoreo de stock
    - 🔔 Alertas automaticas
    - 📦 Procesamiento de pedidos
    - 🔄 Cadena de suministro
    - 📈 Reportes autonomos
    """)
    
    st.markdown("---")
    st.markdown(f"**Ultima ejecucion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== METRICAS INICIALES ====================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Productos", len(inventario_df) if not inventario_df.empty else 0)
with col2:
    if not inventario_df.empty and 'Cantidad' in inventario_df.columns:
        if 'Min_stock' in inventario_df.columns:
            stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= inventario_df['Min_stock']])
        else:
            stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= 10])
        st.metric("Stock Critico", stock_bajo, delta="Requiere atencion" if stock_bajo > 0 else None)
    else:
        st.metric("Stock Critico", 0)
with col3:
    st.metric("Proveedores", len(proveedores_df) if not proveedores_df.empty else 0)

st.divider()

# ==================== BOTON PRINCIPAL ====================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("🤖 Ejecutar Agente Inteligente", use_container_width=True):
        with st.spinner("Agente inteligente analizando el sistema..."):
            resultado = agente.ejecutar()
            
            # Mostrar resultados
            st.success(f"✅ Agente completado exitosamente")
            
            # Metricas de resultado
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Alertas Detectadas", resultado['alertas'])
            with col_r2:
                st.metric("Pedidos Procesados", resultado['pedidos'])
            with col_r3:
                st.metric("Tareas Ejecutadas", len(agente.tareas))
            
            # Mostrar pedidos generados
            if resultado['detalles']:
                st.markdown("---")
                st.markdown("### 📦 Pedidos Automaticos Generados")
                
                for pedido in resultado['detalles']:
                    with st.expander(f" Pedido: {pedido['producto']}"):
                        col_p1, col_p2 = st.columns(2)
                        with col_p1:
                            st.write(f"**Cantidad:** {pedido['cantidad']} unidades")
                            st.write(f"**Proveedor:** {pedido['proveedor']}")
                        with col_p2:
                            st.write(f"**Numero Orden:** {pedido['numero_orden']}")
                            st.write(f"**Estado:** {pedido['estado']}")
                        st.write(f"**Fecha:** {pedido['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.info("No se generaron pedidos - Todos los niveles de stock son normales")

st.divider()

# ==================== MONITOREO EN TIEMPO REAL ====================
st.markdown("### 📊 Monitoreo en Tiempo Real")

col_m1, col_m2 = st.columns([1, 1])

with col_m1:
    st.markdown('<div class="card-title">Estado Actual del Stock</div>', unsafe_allow_html=True)
    if st.button("🔄 Actualizar Monitoreo", use_container_width=True):
        alertas = agente.monitorear_stock()
        
        if alertas:
            st.warning(f"⚠️ Se detectaron {len(alertas)} productos con stock critico")
            for alerta in alertas[:10]:
                st.write(f"- **{alerta['producto']}**: Stock {alerta['stock_actual']} (Minimo {alerta['minimo']})")
        else:
            st.success("✅ Todos los niveles de stock son normales")

with col_m2:
    st.markdown('<div class="card-title">Estadisticas del Agente</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-box">
        <strong>📈 Rendimiento del Agente:</strong><br>
        - Total de tareas ejecutadas: {len(agente.tareas)}<br>
        - Ciclos de monitoreo: Activo<br>
        - Estado: Operativo
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== HISTORIAL DE TAREAS ====================
if agente.tareas:
    with st.expander("📜 Ver Historial de Tareas del Agente"):
        historial_df = pd.DataFrame(agente.tareas)
        historial_df['fecha'] = pd.to_datetime(historial_df['fecha'])
        st.dataframe(
            historial_df.sort_values('fecha', ascending=False),
            use_container_width=True,
            column_config={
                "producto": "Producto",
                "cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                "proveedor": "Proveedor",
                "fecha": st.column_config.DatetimeColumn("Fecha"),
                "estado": "Estado",
                "numero_orden": "N° Orden"
            }
        )

# ==================== INFORMACION DE TABLAS ====================
with st.expander(" Ver Datos del Sistema"):
    tab1, tab2 = st.tabs([" Inventario", " Proveedores"])
    
    with tab1:
        if not inventario_df.empty:
            st.dataframe(inventario_df, use_container_width=True)
        else:
            st.info("No hay datos de inventario disponibles")
    
    with tab2:
        if not proveedores_df.empty:
            st.dataframe(proveedores_df, use_container_width=True)
        else:
            st.info("No hay datos de proveedores disponibles")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;">🤖 IA Agentica - Agente Inteligente Autonomo</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Monitoreo Automatico | Procesamiento de Pedidos | Cadena de Suministro Inteligente
    </p>
</div>
""", unsafe_allow_html=True)