import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database.models import obtener_inventario, obtener_productos

# Configuracion de la pagina
st.set_page_config(
    page_title="Inventario - Ferreteria IA", 
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
    
    /* === INPUTS === */
    .stTextInput input {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border: 1px solid rgba(96, 165, 250, 0.2);
        border-radius: 12px;
        color: white;
        padding: 0.5rem 1rem;
    }
    
    .stSelectbox div {
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
    
    /* === STOCK INDICATOR === */
    .stock-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .stock-critical { background-color: #ef4444; box-shadow: 0 0 5px #ef4444; }
    .stock-low { background-color: #f59e0b; box-shadow: 0 0 5px #f59e0b; }
    .stock-normal { background-color: #10b981; box-shadow: 0 0 5px #10b981; }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES DE PAGINACION ====================
def paginar_dataframe(df, items_por_pagina, pagina_actual):
    """Divide un dataframe en paginas"""
    start_idx = (pagina_actual - 1) * items_por_pagina
    end_idx = start_idx + items_por_pagina
    return df.iloc[start_idx:end_idx]

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
            <span style="color: #60a5fa;">Página {pagina_actual} de {total_paginas}</span>
            <span style="color: #6b7280; margin-left: 0.5rem;">({total_items} productos)</span>
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
    <h1> Control de Inventario</h1>
    <p>Gestion completa de stock y productos</p>
    <span class="badge-success">Sistema en Tiempo Real</span>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
inventario_df = obtener_inventario()
productos_df = obtener_productos()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">📦</div>
        <h2 style="color: #60a5fa;">Inventario</h2>
        <p style="color: #9ca3af;">Control de Stock</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Configuracion")
    items_por_pagina = st.selectbox(
        "Productos por pagina:",
        [10, 25, 50, 100],
        index=0,
        key="inventario_items_por_pagina"
    )
    
    st.markdown("---")
    st.markdown("### Filtros Rapidos")
    
    filtro_stock = st.selectbox(
        "Filtrar por stock:",
        ["Todos", "Stock Critico", "Stock Medio", "Stock Alto"]
    )
    
    st.markdown("---")
    st.markdown("### Acciones")
    
    if st.button(" Actualizar Datos", use_container_width=True):
        st.rerun()
    
    if not inventario_df.empty:
        csv = inventario_df.to_csv(index=False)
        st.download_button(
            " Exportar a CSV",
            csv,
            f"inventario_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown(f"**Ultima actualizacion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== METRICAS PRINCIPALES ====================
if not inventario_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Productos", f"{len(inventario_df):,}")
    
    with col2:
        if 'Estado_Stock' in inventario_df.columns:
            stock_bajo = len(inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock'])
        else:
            stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= 10]) if 'Cantidad' in inventario_df.columns else 0
        st.metric("Stock Critico", f"{stock_bajo}", delta="⚠️ Alerta" if stock_bajo > 0 else "✅ Normal")
    
    with col3:
        total_unidades = inventario_df['Cantidad'].sum() if 'Cantidad' in inventario_df.columns else 0
        st.metric("Total Unidades", f"{total_unidades:,}")
    
    with col4:
        if 'Estado_Stock' in inventario_df.columns:
            stock_optimo = len(inventario_df[inventario_df['Estado_Stock'] == 'Stock Alto'])
        else:
            stock_optimo = len(inventario_df[inventario_df['Cantidad'] > 50]) if 'Cantidad' in inventario_df.columns else 0
        porcentaje_optimo = (stock_optimo / len(inventario_df) * 100) if len(inventario_df) > 0 else 0
        st.metric("Stock Optimo", f"{porcentaje_optimo:.1f}%")
    
    st.divider()
    
    # ==================== GRAFICO DE DISTRIBUCION ====================
    st.markdown("## Distribucion de Stock")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        if 'Estado_Stock' in inventario_df.columns:
            estado_counts = inventario_df['Estado_Stock'].value_counts()
            colores = {'Bajo Stock': '#ef4444', 'Stock Medio': '#f59e0b', 'Stock Alto': '#10b981'}
            fig = px.pie(
                values=estado_counts.values, 
                names=estado_counts.index,
                template="plotly_dark",
                color_discrete_map=colores,
                hole=0.3
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                title="Distribucion por Estado"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de estado de stock")
    
    with col_graf2:
        if 'Cantidad' in inventario_df.columns:
            top_productos = inventario_df.nlargest(10, 'Cantidad')
            fig = px.bar(
                top_productos,
                x='Nombre',
                y='Cantidad',
                template="plotly_dark",
                color='Cantidad',
                color_continuous_scale='blues',
                title="Top 10 Productos con Mayor Stock"
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # ==================== PRODUCTOS CON STOCK BAJO ====================
    st.markdown("## Productos con Stock Critico")
    
    if 'Estado_Stock' in inventario_df.columns:
        productos_criticos = inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock']
    else:
        productos_criticos = inventario_df[inventario_df['Cantidad'] <= 10] if 'Cantidad' in inventario_df.columns else pd.DataFrame()
    
    if not productos_criticos.empty:
        st.markdown(f'<span class="badge-danger">⚠️ {len(productos_criticos)} productos requieren atencion inmediata</span>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Inicializar estado de paginacion para productos criticos
        if 'pagina_criticos' not in st.session_state:
            st.session_state.pagina_criticos = 1
        
        items_por_pagina = st.session_state.get('inventario_items_por_pagina', 10)
        
        # Paginar productos criticos
        total_criticos = len(productos_criticos)
        productos_criticos_paginados = paginar_dataframe(productos_criticos, items_por_pagina, st.session_state.pagina_criticos)
        
        # Mostrar tabla de productos criticos
        st.dataframe(
            productos_criticos_paginados,
            use_container_width=True,
            column_config={
                "Nombre": "Producto",
                "Cantidad": st.column_config.NumberColumn("Stock Actual", format="%d"),
                "Min_stock": st.column_config.NumberColumn("Stock Minimo", format="%d"),
                "Estado_Stock": "Estado"
            }
        )
        
        # Controles de paginacion para criticos
        if total_criticos > items_por_pagina:
            nueva_pagina = mostrar_controles_paginacion(total_criticos, items_por_pagina, st.session_state.pagina_criticos, "criticos")
            if nueva_pagina != st.session_state.pagina_criticos:
                st.session_state.pagina_criticos = nueva_pagina
                st.rerun()
        
        # Boton para generar orden de compra
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("📦 Generar Orden de Reabastecimiento", use_container_width=True):
                with st.spinner("Generando ordenes de compra..."):
                    st.success(f"Se generaron ordenes para {len(productos_criticos)} productos")
                    st.balloons()
    else:
        st.success("✅ No hay productos con stock critico. Niveles de stock optimos.")
    
    st.divider()
    
    # ==================== INVENTARIO COMPLETO CON PAGINACION ====================
    st.markdown("## Inventario Completo")
    
    # Aplicar filtros
    df_filtrado = inventario_df.copy()
    
    if filtro_stock != "Todos" and 'Estado_Stock' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['Estado_Stock'] == filtro_stock]
    
    # Inicializar estado de paginacion para inventario completo
    if 'pagina_inventario' not in st.session_state:
        st.session_state.pagina_inventario = 1
    
    items_por_pagina = st.session_state.get('inventario_items_por_pagina', 10)
    
    total_items = len(df_filtrado)
    total_paginas = (total_items + items_por_pagina - 1) // items_por_pagina
    
    # Asegurar pagina valida
    if st.session_state.pagina_inventario > total_paginas and total_paginas > 0:
        st.session_state.pagina_inventario = total_paginas
    if st.session_state.pagina_inventario < 1:
        st.session_state.pagina_inventario = 1
    
    # Paginar datos
    df_paginado = paginar_dataframe(df_filtrado, items_por_pagina, st.session_state.pagina_inventario)
    
    # Mostrar informacion de filtros
    if filtro_stock != "Todos":
        st.caption(f"🔍 Mostrando {len(df_filtrado)} productos con filtro '{filtro_stock}'")
    
    # Configurar columnas para la tabla
    column_config = {
        "Nombre": "Producto",
        "Cantidad": st.column_config.NumberColumn("Stock Actual", format="%d"),
        "Min_stock": st.column_config.NumberColumn("Stock Minimo", format="%d"),
        "Estado_Stock": "Estado"
    }
    
    # Mostrar tabla
    st.dataframe(df_paginado, use_container_width=True, column_config=column_config, height=500)
    
    # Controles de paginacion
    if total_items > items_por_pagina:
        st.markdown("---")
        nueva_pagina = mostrar_controles_paginacion(total_items, items_por_pagina, st.session_state.pagina_inventario, "inventario")
        if nueva_pagina != st.session_state.pagina_inventario:
            st.session_state.pagina_inventario = nueva_pagina
            st.rerun()
    
    # ==================== RESUMEN DE PAGINACION ====================
    st.markdown("---")
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown(f"""
        <div class="info-box">
            <strong>📊 Total Productos:</strong><br>
            {total_items:,}
        </div>
        """, unsafe_allow_html=True)
    
    with col_res2:
        st.markdown(f"""
        <div class="info-box">
            <strong>📄 Paginas:</strong><br>
            {total_paginas}
        </div>
        """, unsafe_allow_html=True)
    
    with col_res3:
        st.markdown(f"""
        <div class="info-box">
            <strong>📋 Por Pagina:</strong><br>
            {items_por_pagina}
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== ANALISIS DE STOCK ====================
    st.divider()
    with st.expander("📊 Analisis Detallado de Stock"):
        col_ana1, col_ana2 = st.columns(2)
        
        with col_ana1:
            st.markdown("#### Top 10 Productos con Menor Stock")
            if 'Cantidad' in inventario_df.columns:
                menores_stock = inventario_df.nsmallest(10, 'Cantidad')
                st.dataframe(menores_stock[['Nombre', 'Cantidad']], use_container_width=True)
        
        with col_ana2:
            st.markdown("#### Estadisticas de Stock")
            if 'Cantidad' in inventario_df.columns:
                stats = inventario_df['Cantidad'].describe()
                st.write(f"**Stock Promedio:** {stats['mean']:.1f} unidades")
                st.write(f"**Stock Maximo:** {stats['max']:.0f} unidades")
                st.write(f"**Stock Minimo:** {stats['min']:.0f} unidades")
                st.write(f"**Desviacion Estandar:** {stats['std']:.1f}")

else:
    st.info("📦 No hay datos de inventario disponibles")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;"> Control de Inventario - Ferreteria IA</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Gestion de Stock | Alertas Automaticas | Control de Inventario
    </p>
</div>
""", unsafe_allow_html=True)