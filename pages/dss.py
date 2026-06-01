import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database.models import obtener_inventario, obtener_facturas, obtener_productos

# Configuracion de la pagina
st.set_page_config(
    page_title="DSS - Decision Support System", 
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
    
    .badge-danger {
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
    
    /* === PAGINACION === */
    .pagination-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        margin: 1rem 0;
        padding: 0.5rem;
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 16px;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    .pagination-info {
        color: #9ca3af;
        font-size: 0.9rem;
        margin: 0 1rem;
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
    
    /* === INFO BOX === */
    .info-box {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #60a5fa;
        color: #cbd5e1;
    }
    
    /* === RECOMMENDATION CARD === */
    .rec-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(96, 165, 250, 0.2);
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

# ==================== FUNCIONES DE PAGINACION ====================
def paginar_lista(items, items_por_pagina, pagina_actual):
    """Divide una lista en paginas"""
    start_idx = (pagina_actual - 1) * items_por_pagina
    end_idx = start_idx + items_por_pagina
    return items[start_idx:end_idx]

def mostrar_controles_paginacion(total_items, items_por_pagina, pagina_actual, key_prefix):
    """Muestra controles de paginacion y retorna la nueva pagina"""
    total_paginas = (total_items + items_por_pagina - 1) // items_por_pagina
    
    if total_paginas <= 1:
        return pagina_actual
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("⏮", key=f"{key_prefix}_first", use_container_width=True):
            return 1
    with col2:
        if st.button("◀", key=f"{key_prefix}_prev", use_container_width=True):
            return max(1, pagina_actual - 1)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 0.3rem;">
            <span style="color: #60a5fa;">Pág. {pagina_actual} de {total_paginas}</span>
            <span style="color: #6b7280; margin-left: 0.5rem;">({total_items} items)</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if st.button("▶", key=f"{key_prefix}_next", use_container_width=True):
            return min(total_paginas, pagina_actual + 1)
    with col5:
        if st.button("⏭", key=f"{key_prefix}_last", use_container_width=True):
            return total_paginas
    
    return pagina_actual

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1> Sistema de Apoyo a Decisiones (DSS)</h1>
    <p>Decisiones inteligentes basadas en datos y analisis predictivo</p>
    <span class="badge-success">Sistema de Decisiones Activo</span>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
inventario_df = obtener_inventario()
facturas_df = obtener_facturas()
productos_df = obtener_productos()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;"></div>
        <h2 style="color: #60a5fa;">DSS - IA</h2>
        <p style="color: #9ca3af;">Decision Support System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Configuracion de Paginacion")
    items_por_pagina = st.selectbox(
        "Items por pagina:",
        [5, 10, 20, 50],
        index=0,
        key="dss_items_por_pagina"
    )
    
    st.markdown("---")
    st.markdown("### Metricas del Sistema")
    
    if not inventario_df.empty:
        if 'Min_stock' in inventario_df.columns:
            stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= inventario_df['Min_stock']])
        else:
            stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= 10])
        st.metric("Productos Criticos", stock_bajo, delta="Requiere atencion" if stock_bajo > 0 else None)
    
    if not facturas_df.empty and 'Total' in facturas_df.columns:
        st.metric("Ventas Totales", f"C$ {facturas_df['Total'].sum():,.2f}")
        st.metric("Ticket Promedio", f"C$ {facturas_df['Total'].mean():,.2f}")
    
    st.markdown("---")
    st.markdown(f"**Ultima actualizacion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== METRICAS CLAVE ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    if not inventario_df.empty:
        total_productos = len(inventario_df)
        st.metric("Total Productos", f"{total_productos:,}")
    else:
        st.metric("Total Productos", "N/A")

with col2:
    if not inventario_df.empty and 'Cantidad' in inventario_df.columns:
        total_unidades = inventario_df['Cantidad'].sum()
        st.metric("Unidades en Stock", f"{total_unidades:,}")
    else:
        st.metric("Unidades en Stock", "N/A")

with col3:
    if not facturas_df.empty:
        total_ventas = len(facturas_df)
        st.metric("Total Ventas", f"{total_ventas:,}")
    else:
        st.metric("Total Ventas", "N/A")

with col4:
    if not facturas_df.empty and 'Total' in facturas_df.columns:
        ingreso_total = facturas_df['Total'].sum()
        st.metric("Ingresos Totales", f"C$ {ingreso_total:,.2f}")
    else:
        st.metric("Ingresos Totales", "N/A")

st.divider()

# ==================== ALERTAS DEL SISTEMA CON PAGINACION ====================
st.markdown("## Alertas del Sistema")

if not inventario_df.empty:
    if 'Cantidad' in inventario_df.columns and 'Min_stock' in inventario_df.columns:
        productos_criticos = inventario_df[inventario_df['Cantidad'] <= inventario_df['Min_stock']]
        
        if len(productos_criticos) > 0:
            st.markdown(f'<span class="badge-danger">⚠️ {len(productos_criticos)} Alertas Criticas</span>', unsafe_allow_html=True)
            st.markdown("---")
            
            # Inicializar estado de paginacion para alertas
            if 'pagina_alertas' not in st.session_state:
                st.session_state.pagina_alertas = 1
            
            items_por_pagina = st.session_state.get('dss_items_por_pagina', 10)
            
            # Convertir a lista para paginacion
            alertas_lista = []
            for _, producto in productos_criticos.iterrows():
                nombre = producto['Nombre'] if 'Nombre' in producto.index else "Producto desconocido"
                alertas_lista.append({
                    'nombre': nombre,
                    'stock': producto['Cantidad'],
                    'minimo': producto['Min_stock']
                })
            
            total_alertas = len(alertas_lista)
            total_paginas = (total_alertas + items_por_pagina - 1) // items_por_pagina
            
            # Asegurar pagina valida
            if st.session_state.pagina_alertas > total_paginas and total_paginas > 0:
                st.session_state.pagina_alertas = total_paginas
            
            # Paginar alertas
            alertas_paginadas = paginar_lista(alertas_lista, items_por_pagina, st.session_state.pagina_alertas)
            
            # Mostrar alertas paginadas
            for alerta in alertas_paginadas:
                st.error(f"🚨 ALERTA CRITICA: **{alerta['nombre']}** - Stock: {alerta['stock']} unidades (Minimo: {alerta['minimo']})")
            
            # Mostrar controles de paginacion
            if total_alertas > items_por_pagina:
                nueva_pagina = mostrar_controles_paginacion(total_alertas, items_por_pagina, st.session_state.pagina_alertas, "alertas")
                if nueva_pagina != st.session_state.pagina_alertas:
                    st.session_state.pagina_alertas = nueva_pagina
                    st.rerun()
        else:
            st.markdown('<span class="badge-success">✅ Sin Alertas Activas</span>', unsafe_allow_html=True)
            st.success("Todos los niveles de stock son normales")
    elif 'Cantidad' in inventario_df.columns:
        productos_criticos = inventario_df[inventario_df['Cantidad'] <= 10]
        if len(productos_criticos) > 0:
            for _, producto in productos_criticos.iterrows():
                nombre = producto['Nombre'] if 'Nombre' in producto.index else "Producto desconocido"
                st.warning(f"⚠️ ALERTA: **{nombre}** - Stock bajo: {producto['Cantidad']} unidades")
else:
    st.info("No hay datos de inventario disponibles")

st.divider()

# ==================== RECOMENDACIONES AUTOMATICAS CON PAGINACION ====================
st.markdown("## Recomendaciones Automaticas")

col_rec1, col_rec2 = st.columns(2)

with col_rec1:
    st.markdown('<div class="card-title"> Compras Recomendadas</div>', unsafe_allow_html=True)
    
    if not inventario_df.empty:
        if 'Cantidad' in inventario_df.columns and 'Min_stock' in inventario_df.columns:
            productos_bajos = inventario_df[inventario_df['Cantidad'] <= inventario_df['Min_stock'] * 1.5]
            
            if len(productos_bajos) > 0:
                # Inicializar estado de paginacion para recomendaciones
                if 'pagina_recomendaciones' not in st.session_state:
                    st.session_state.pagina_recomendaciones = 1
                
                items_por_pagina = st.session_state.get('dss_items_por_pagina', 10)
                
                # Convertir a lista para paginacion
                recomendaciones_lista = []
                for _, prod in productos_bajos.iterrows():
                    cantidad_recomendada = prod['Min_stock'] * 2 - prod['Cantidad']
                    if cantidad_recomendada > 0:
                        nombre = prod['Nombre'] if 'Nombre' in prod.index else "Producto"
                        urgencia = "🔴 Urgente" if prod['Cantidad'] <= prod['Min_stock'] else "🟡 Normal"
                        recomendaciones_lista.append({
                            'nombre': nombre,
                            'cantidad': int(cantidad_recomendada),
                            'urgencia': urgencia
                        })
                
                total_recomendaciones = len(recomendaciones_lista)
                
                if total_recomendaciones > 0:
                    # Paginar recomendaciones
                    recomendaciones_paginadas = paginar_lista(recomendaciones_lista, items_por_pagina, st.session_state.pagina_recomendaciones)
                    
                    # Mostrar recomendaciones paginadas
                    for rec in recomendaciones_paginadas:
                        st.markdown(f"""
                        <div class="rec-card">
                            <strong>{rec['nombre']}</strong><br>
                            📦 Comprar: {rec['cantidad']} unidades<br>
                            {rec['urgencia']}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Mostrar controles de paginacion
                    if total_recomendaciones > items_por_pagina:
                        total_paginas = (total_recomendaciones + items_por_pagina - 1) // items_por_pagina
                        if st.session_state.pagina_recomendaciones > total_paginas:
                            st.session_state.pagina_recomendaciones = total_paginas
                        
                        nueva_pagina = mostrar_controles_paginacion(total_recomendaciones, items_por_pagina, st.session_state.pagina_recomendaciones, "recomendaciones")
                        if nueva_pagina != st.session_state.pagina_recomendaciones:
                            st.session_state.pagina_recomendaciones = nueva_pagina
                            st.rerun()
                else:
                    st.success("No se requieren compras inmediatas")
            else:
                st.success("No se requieren compras inmediatas")
        elif 'Cantidad' in inventario_df.columns:
            productos_bajos = inventario_df[inventario_df['Cantidad'] <= 20]
            for _, prod in productos_bajos.head(10).iterrows():
                nombre = prod['Nombre'] if 'Nombre' in prod.index else "Producto"
                st.write(f"- {nombre}: Stock actual {prod['Cantidad']} - Recomendar compra")
    else:
        st.info("No hay datos de inventario")

with col_rec2:
    st.markdown('<div class="card-title"> Analisis de Ventas</div>', unsafe_allow_html=True)
    
    if not facturas_df.empty and 'Total' in facturas_df.columns:
        promedio_ventas = facturas_df['Total'].mean()
        ventas_totales = facturas_df['Total'].sum()
        num_ventas = len(facturas_df)
        
        st.metric("Ticket Promedio", f"C$ {promedio_ventas:,.2f}")
        st.metric("Total Ventas", f"C$ {ventas_totales:,.2f}")
        st.metric("Numero Transacciones", f"{num_ventas:,}")
        
        if promedio_ventas < 200:
            st.warning("📉 Recomendacion: Implementar promociones para aumentar el ticket promedio")
        elif promedio_ventas > 500:
            st.success("✅ Ticket promedio excelente - Mantener estrategia")
        else:
            st.info("📊 Ticket promedio adecuado - Considerar small upgrades")
        
        if num_ventas < 100:
            st.info("📢 Recomendacion: Aumentar campañas de marketing")
    else:
        st.info("No hay datos de ventas suficientes para analizar")

st.divider()

# ==================== DECISIONES ESTRATEGICAS ====================
st.markdown("## Decisiones Estrategicas")

col_est1, col_est2 = st.columns([1, 2])

with col_est1:
    decision = st.selectbox(
        "Seleccione area de analisis:",
        [" Optimizacion de inventario", " Estrategia de precios", " Promociones y marketing", " Gestion de proveedores"]
    )

with col_est2:
    if decision == " Optimizacion de inventario":
        if not inventario_df.empty:
            total_productos = len(inventario_df)
            if 'Min_stock' in inventario_df.columns:
                stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= inventario_df['Min_stock']])
            else:
                stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= 10])
            
            st.markdown(f"""
            <div class="info-box">
                <strong>📊 Analisis de Inventario</strong><br><br>
                - Total productos: {total_productos}<br>
                - Productos con stock critico: {stock_bajo}<br>
                - Porcentaje critico: {(stock_bajo/total_productos)*100:.1f}%<br><br>
                <strong>🎯 Recomendacion:</strong><br>
                Establecer sistema de puntos de reorden automaticos para {stock_bajo} productos criticos.
                Implementar alertas preventivas cuando el stock llegue al 150% del minimo.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos de inventario disponibles")

    elif decision == " Estrategia de precios":
        if not facturas_df.empty and 'Total' in facturas_df.columns:
            promedio = facturas_df['Total'].mean()
            percentiles = facturas_df['Total'].quantile([0.25, 0.5, 0.75])
            
            st.markdown(f"""
            <div class="info-box">
                <strong>💰 Analisis de Precios</strong><br><br>
                - Ticket promedio: C$ {promedio:,.2f}<br>
                - Percentil 25: C$ {percentiles[0.25]:,.2f}<br>
                - Percentil 50: C$ {percentiles[0.5]:,.2f}<br>
                - Percentil 75: C$ {percentiles[0.75]:,.2f}<br><br>
                <strong>🎯 Recomendacion:</strong><br>
                {'Implementar descuentos por volumen para aumentar ticket' if promedio < 300 else 'Mantener precios actuales, considerar premium para productos top'}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos de ventas suficientes")

    elif decision == " Promociones y marketing":
        if not facturas_df.empty:
            num_ventas = len(facturas_df)
            st.markdown(f"""
            <div class="info-box">
                <strong>📢 Analisis de Marketing</strong><br><br>
                - Volumen de ventas: {num_ventas} transacciones<br>
                - Frecuencia promedio: {num_ventas/30:.1f} ventas/dia<br><br>
                <strong>🎯 Recomendacion:</strong><br>
                {'Lanzar campaña de fidelizacion para clientes frecuentes' if num_ventas > 50 else 'Aumentar presencia en redes sociales y ofrecer promociones de lanzamiento'}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos de ventas disponibles")

    else:
        st.markdown("""
        <div class="info-box">
            <strong>🏭 Analisis de Proveedores</strong><br><br>
            <strong>🎯 Recomendacion:</strong><br>
            - Evaluar rendimiento de proveedores mensualmente<br>
            - Negociar descuentos por volumen con proveedores clave<br>
            - Diversificar fuentes de suministro para productos criticos<br>
            - Establecer contratos a largo plazo para mejores precios
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ==================== SIMULADOR DE DECISIONES ====================
with st.expander(" Simulador de Decisiones (What-If Analysis)"):
    st.markdown("### Simular impacto de decisiones")
    
    col_sim1, col_sim2, col_sim3 = st.columns(3)
    
    with col_sim1:
        incremento_precio = st.slider("Incremento de precios (%)", -20, 50, 0)
    
    with col_sim2:
        inversion_marketing = st.slider("Inversion en marketing (C$)", 0, 10000, 1000, step=500)
    
    with col_sim3:
        mejora_stock = st.slider("Reduccion de stock critico (%)", 0, 100, 50)
    
    if st.button("Calcular Impacto Estimado", use_container_width=True):
        if not facturas_df.empty and 'Total' in facturas_df.columns:
            ventas_actuales = facturas_df['Total'].sum()
            
            impacto_precio = ventas_actuales * (incremento_precio / 100)
            impacto_marketing = inversion_marketing * 1.5
            
            nuevo_total = ventas_actuales + impacto_precio + impacto_marketing
            
            st.markdown(f"""
            <div class="info-box">
                <strong>📈 Resultados de la Simulacion:</strong><br><br>
                - Ventas actuales: C$ {ventas_actuales:,.2f}<br>
                - Impacto por precio: C$ {impacto_precio:,.2f}<br>
                - Impacto por marketing: C$ {impacto_marketing:,.2f}<br>
                - <strong>Nuevo total estimado: C$ {nuevo_total:,.2f}</strong><br>
                - <strong>Crecimiento: {((nuevo_total/ventas_actuales)-1)*100:.1f}%</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No hay datos de ventas para simular")

st.divider()

# ==================== REPORTE EJECUTIVO ====================
with st.expander(" 📊 Generar Reporte Ejecutivo"):
    if st.button("Generar Reporte DSS", use_container_width=True):
        with st.spinner("Generando reporte ejecutivo..."):
            reporte = f"""
            ========================================
            REPORTE DSS - FERRETERIA IA
            ========================================
            Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            --- METRICAS GENERALES ---
            Total Productos: {len(inventario_df) if not inventario_df.empty else 0}
            Total Ventas: {len(facturas_df) if not facturas_df.empty else 0}
            Ingresos Totales: C$ {facturas_df['Total'].sum() if not facturas_df.empty and 'Total' in facturas_df.columns else 0:,.2f}
            
            --- RECOMENDACIONES PRIORITARIAS ---
            1. Revisar productos con stock critico
            2. Analizar estrategia de precios
            3. Evaluar campañas promocionales
            
            --- ACCIONES SUGERIDAS ---
            - Implementar sistema de alertas automaticas
            - Establecer puntos de reorden
            - Monitorear tendencias de ventas
            ========================================
            """
            st.code(reporte, language="text")
            st.success("Reporte generado exitosamente")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;"> DSS - Decision Support System</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Alertas Automaticas | Recomendaciones Inteligentes | Analisis Estrategico | Paginacion Integrada
    </p>
</div>
""", unsafe_allow_html=True)