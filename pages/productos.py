import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database.models import obtener_productos, obtener_inventario

# Configuracion de la pagina
st.set_page_config(
    page_title="Productos - Ferreteria IA", 
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
    
    /* === CATEGORY CARD === */
    .category-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        border: 1px solid rgba(96, 165, 250, 0.2);
        transition: all 0.3s ease;
    }
    
    .category-card:hover {
        transform: translateY(-3px);
        border-color: rgba(96, 165, 250, 0.5);
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
    <h1> Catalogo de Productos</h1>
    <p>Gestion completa del catalogo de productos</p>
    <span class="badge-success">Sistema de Gestion</span>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
productos_df = obtener_productos()
inventario_df = obtener_inventario()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">📦</div>
        <h2 style="color: #60a5fa;">Productos</h2>
        <p style="color: #9ca3af;">Catalogo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Configuracion")
    items_por_pagina = st.selectbox(
        "Productos por pagina:",
        [10, 25, 50, 100, 200],
        index=0,
        key="productos_items_por_pagina"
    )
    
    st.markdown("---")
    
    st.markdown("### Acciones")
    if st.button(" Actualizar Datos", use_container_width=True):
        st.rerun()
    
    if not productos_df.empty:
        csv = productos_df.to_csv(index=False)
        st.download_button(
            " Exportar a CSV",
            csv,
            f"productos_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown(f"**Ultima actualizacion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== METRICAS PRINCIPALES ====================
if not productos_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Productos", f"{len(productos_df):,}")
    
    with col2:
        if 'Categoria' in productos_df.columns:
            num_categorias = productos_df['Categoria'].nunique()
            st.metric("Categorias", f"{num_categorias:,}")
        else:
            st.metric("Categorias", "N/A")
    
    with col3:
        if 'Precio' in productos_df.columns:
            precio_promedio = productos_df['Precio'].mean()
            st.metric("Precio Promedio", f"C$ {precio_promedio:,.2f}")
        else:
            st.metric("Precio Promedio", "N/A")
    
    with col4:
        if not inventario_df.empty:
            total_stock = inventario_df['Cantidad'].sum() if 'Cantidad' in inventario_df.columns else 0
            st.metric("Total Unidades Stock", f"{total_stock:,}")
        else:
            st.metric("Total Unidades Stock", "N/A")
    
    st.divider()
    
    # ==================== CATEGORIAS ====================
    if 'Categoria' in productos_df.columns:
        st.markdown("## Categorias")
        categorias_counts = productos_df['Categoria'].value_counts()
        
        # Mostrar categorias en grid
        cols_cat = st.columns(min(len(categorias_counts), 4))
        for i, (cat, count) in enumerate(categorias_counts.items()):
            with cols_cat[i % 4]:
                st.markdown(f"""
                <div class="category-card">
                    <div style="font-size: 1.5rem;">📁</div>
                    <strong>{cat}</strong><br>
                    <span style="color: #9ca3af;">{count} productos</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
    
    # ==================== BUSCADOR Y FILTROS ====================
    st.markdown("## Buscar y Filtrar Productos")
    
    col_busq1, col_busq2, col_busq3 = st.columns([2, 1, 1])
    
    with col_busq1:
        busqueda = st.text_input("", placeholder="🔍 Buscar por nombre, categoria o descripcion...")
    
    with col_busq2:
        if 'Categoria' in productos_df.columns:
            categoria_filtro = st.selectbox("Categoria:", ["Todas"] + list(productos_df['Categoria'].unique()))
        else:
            categoria_filtro = "Todas"
    
    with col_busq3:
        ordenar_por = st.selectbox("Ordenar por:", ["Nombre", "Precio (asc)", "Precio (desc)"])
    
    # Aplicar filtros
    df_filtrado = productos_df.copy()
    
    if busqueda:
        mask = df_filtrado.apply(lambda row: busqueda.lower() in str(row.values).lower(), axis=1)
        df_filtrado = df_filtrado[mask]
    
    if categoria_filtro != "Todas" and 'Categoria' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['Categoria'] == categoria_filtro]
    
    if ordenar_por == "Nombre" and 'Nombre' in df_filtrado.columns:
        df_filtrado = df_filtrado.sort_values('Nombre')
    elif ordenar_por == "Precio (asc)" and 'Precio' in df_filtrado.columns:
        df_filtrado = df_filtrado.sort_values('Precio')
    elif ordenar_por == "Precio (desc)" and 'Precio' in df_filtrado.columns:
        df_filtrado = df_filtrado.sort_values('Precio', ascending=False)
    
    # Mostrar resultados de busqueda
    if busqueda or categoria_filtro != "Todas":
        st.caption(f"🔎 Se encontraron {len(df_filtrado)} resultados")
    
    st.divider()
    
    # ==================== TABLA DE PRODUCTOS CON PAGINACION ====================
    st.markdown("## Listado de Productos")
    
    # Inicializar estado de paginacion
    if 'pagina_productos' not in st.session_state:
        st.session_state.pagina_productos = 1
    
    items_por_pagina = st.session_state.get('productos_items_por_pagina', 25)
    
    total_items = len(df_filtrado)
    total_paginas = (total_items + items_por_pagina - 1) // items_por_pagina
    
    # Asegurar pagina valida
    if st.session_state.pagina_productos > total_paginas and total_paginas > 0:
        st.session_state.pagina_productos = total_paginas
    if st.session_state.pagina_productos < 1:
        st.session_state.pagina_productos = 1
    
    # Paginar datos
    df_paginado = paginar_dataframe(df_filtrado, items_por_pagina, st.session_state.pagina_productos)
    
    # Configurar columnas para la tabla
    column_config = {
        "id": st.column_config.NumberColumn("ID", format="%d"),
        "nombre": st.column_config.TextColumn("Nombre"),
        "categoria": st.column_config.TextColumn("Categoria"),
        "precio": st.column_config.NumberColumn("Precio", format="C$ %.2f"),
        "stock": st.column_config.NumberColumn("Stock", format="%d"),
        "descripcion": st.column_config.TextColumn("Descripcion"),
    }
    
    # Mostrar tabla
    st.dataframe(df_paginado, use_container_width=True, column_config=column_config, height=500)
    
    # Controles de paginacion
    if total_items > items_por_pagina:
        st.markdown("---")
        nueva_pagina = mostrar_controles_paginacion(total_items, items_por_pagina, st.session_state.pagina_productos, "productos")
        if nueva_pagina != st.session_state.pagina_productos:
            st.session_state.pagina_productos = nueva_pagina
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
            <strong>📄 Total Paginas:</strong><br>
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
    
    # ==================== ANALISIS DE PRECIOS ====================
    st.divider()
    with st.expander("📊 Analisis de Precios"):
        if 'Precio' in productos_df.columns:
            col_prec1, col_prec2 = st.columns(2)
            
            with col_prec1:
                # Distribucion de precios
                fig = px.histogram(
                    productos_df, 
                    x='Precio', 
                    nbins=20,
                    title="Distribucion de Precios",
                    template="plotly_dark",
                    color_discrete_sequence=['#3b82f6']
                )
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
            
            with col_prec2:
                # Estadisticas de precios
                stats = productos_df['Precio'].describe()
                st.markdown(f"""
                <div class="info-box">
                    <strong>📈 Estadisticas de Precios:</strong><br><br>
                    - Precio Minimo: C$ {stats['min']:,.2f}<br>
                    - Precio Maximo: C$ {stats['max']:,.2f}<br>
                    - Precio Promedio: C$ {stats['mean']:,.2f}<br>
                    - Mediana: C$ {stats['50%']:,.2f}<br>
                    - Desviacion Estandar: C$ {stats['std']:,.2f}
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("📦 No hay datos de productos disponibles")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;"> Catalogo de Productos - Ferreteria IA</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Gestion de Productos | Categorias | Control de Stock
    </p>
</div>
""", unsafe_allow_html=True)