import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database.models import obtener_clientes, obtener_facturas

# Configuracion de la pagina
st.set_page_config(
    page_title="Clientes - Ferreteria IA", 
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
    
    .pagination-btn {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.3rem 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .pagination-btn:hover {
        transform: scale(1.05);
    }
    
    .pagination-info {
        color: #9ca3af;
        font-size: 0.9rem;
        margin: 0 1rem;
    }
    
    /* === BADGES === */
    .badge {
        background: linear-gradient(135deg, #059669, #047857);
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
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 16px;
        margin-top: 2rem;
    }
    
    hr {
        border-color: rgba(96, 165, 250, 0.2);
        margin: 1.5rem 0;
    }
    
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
    <h1> Gestion de Clientes</h1>
    <p>Administracion completa de clientes - Historial, estadisticas y analisis</p>
    <span class="badge">Sistema de Gestion</span>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
clientes_df = obtener_clientes()
facturas_df = obtener_facturas()

# ==================== FUNCION DE PAGINACION ====================
def paginar_dataframe(df, items_por_pagina, pagina_actual):
    """Divide un dataframe en paginas"""
    start_idx = (pagina_actual - 1) * items_por_pagina
    end_idx = start_idx + items_por_pagina
    return df.iloc[start_idx:end_idx]

def mostrar_paginacion(total_items, items_por_pagina, pagina_actual, key_prefix=""):
    """Muestra controles de paginacion"""
    total_paginas = (total_items + items_por_pagina - 1) // items_por_pagina
    
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("⏮ Primera", key=f"{key_prefix}_first", use_container_width=True):
            return 1
    with col2:
        if st.button("◀ Anterior", key=f"{key_prefix}_prev", use_container_width=True):
            return max(1, pagina_actual - 1)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem; background: linear-gradient(135deg, #1e1e2e, #2d2d3f); border-radius: 8px;">
            <span style="color: #60a5fa;">Página {pagina_actual} de {total_paginas}</span>
            <span style="color: #6b7280; margin-left: 0.5rem;">({total_items} registros)</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if st.button("Siguiente ▶", key=f"{key_prefix}_next", use_container_width=True):
            return min(total_paginas, pagina_actual + 1)
    with col5:
        if st.button("Última ⏭", key=f"{key_prefix}_last", use_container_width=True):
            return total_paginas
    
    return pagina_actual

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;"></div>
        <h2 style="color: #60a5fa;">Clientes</h2>
        <p style="color: #9ca3af;">Modulo de Gestion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Configuracion de Pagina")
    items_por_pagina = st.selectbox(
        "Registros por pagina:",
        [10, 25, 50, 100, 200],
        index=0,
        key="items_por_pagina_sidebar"
    )
    
    st.markdown("---")
    st.markdown("### Acciones Rapidas")
    
    if st.button(" Actualizar Datos", use_container_width=True):
        st.rerun()
    
    if not clientes_df.empty:
        csv = clientes_df.to_csv(index=False)
        st.download_button(
            " Exportar a CSV",
            csv,
            f"clientes_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("### Estadisticas")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d3f); border-radius: 12px; padding: 1rem; text-align: center;">
        <div style="font-size: 2rem; font-weight: bold; color: #fbbf24;">{len(clientes_df):,}</div>
        <div style="color: #9ca3af;">Total Clientes</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== METRICAS PRINCIPALES ====================
if not clientes_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Clientes", f"{len(clientes_df):,}")
    
    with col2:
        nuevos = min(5, len(clientes_df))
        st.metric("Clientes Nuevos", f"+{nuevos}", delta="Ultimo mes")
    
    with col3:
        if not facturas_df.empty and 'Idcliente' in facturas_df.columns:
            clientes_activos = facturas_df['Idcliente'].nunique()
            st.metric("Clientes Activos", f"{clientes_activos:,}")
        else:
            st.metric("Clientes Activos", "N/A")
    
    with col4:
        if not facturas_df.empty and 'Total' in facturas_df.columns:
            ticket_promedio = facturas_df['Total'].mean()
            st.metric("Ticket Promedio", f"C$ {ticket_promedio:,.2f}")
        else:
            st.metric("Ticket Promedio", "N/A")
    
    st.divider()
    
    # ==================== BUSCADOR Y FILTROS ====================
    st.markdown("### 🔍 Buscar y Filtrar Clientes")
    
    col_busq1, col_busq2 = st.columns([3, 1])
    
    with col_busq1:
        busqueda = st.text_input("", placeholder="Buscar por nombre, email, telefono o direccion...")
    
    with col_busq2:
        filtro_columna = st.selectbox(
            "Filtrar por:",
            ["Todos", "Nombre", "Email", "Telefono"]
        )
    
    # Aplicar filtros
    clientes_filtrados = clientes_df.copy()
    
    if busqueda:
        mask = clientes_filtrados.apply(lambda row: busqueda.lower() in str(row.values).lower(), axis=1)
        clientes_filtrados = clientes_filtrados[mask]
    
    if filtro_columna != "Todos" and filtro_columna in clientes_filtrados.columns:
        clientes_filtrados = clientes_filtrados[clientes_filtrados[filtro_columna].notna()]
    
    # Mostrar resultados de busqueda
    if busqueda:
        st.caption(f"🔎 Se encontraron {len(clientes_filtrados)} resultados para '{busqueda}'")
    
    st.divider()
    
    # ==================== TABLA DE CLIENTES CON PAGINACION ====================
    st.markdown("### 📋 Listado de Clientes")
    
    # Inicializar estado de paginacion
    if 'pagina_clientes' not in st.session_state:
        st.session_state.pagina_clientes = 1
    
    # Obtener items por pagina desde sidebar
    items_por_pagina = st.session_state.get('items_por_pagina_sidebar', 25)
    
    # Calcular total de paginas
    total_clientes = len(clientes_filtrados)
    total_paginas = (total_clientes + items_por_pagina - 1) // items_por_pagina
    
    # Asegurar que la pagina actual sea valida
    if st.session_state.pagina_clientes > total_paginas and total_paginas > 0:
        st.session_state.pagina_clientes = total_paginas
    if st.session_state.pagina_clientes < 1:
        st.session_state.pagina_clientes = 1
    
    # Paginar datos
    clientes_paginados = paginar_dataframe(clientes_filtrados, items_por_pagina, st.session_state.pagina_clientes)
    
    # Mostrar tabla
    column_config = {
        "id": st.column_config.NumberColumn("ID", format="%d"),
        "nombre": st.column_config.TextColumn("Nombre"),
        "email": st.column_config.TextColumn("Email"),
        "telefono": st.column_config.TextColumn("Telefono"),
        "direccion": st.column_config.TextColumn("Direccion"),
    }
    
    st.dataframe(
        clientes_paginados,
        use_container_width=True,
        column_config=column_config,
        height=450
    )
    
    # Mostrar controles de paginacion
    if total_clientes > items_por_pagina:
        st.markdown("---")
        
        col_pag1, col_pag2, col_pag3 = st.columns([1, 2, 1])
        
        with col_pag1:
            # Selector de pagina directa
            pagina_manual = st.number_input(
                "Ir a pagina:",
                min_value=1,
                max_value=total_paginas,
                value=st.session_state.pagina_clientes,
                step=1,
                key="pagina_manual"
            )
            if pagina_manual != st.session_state.pagina_clientes:
                st.session_state.pagina_clientes = pagina_manual
                st.rerun()
        
        with col_pag2:
            # Botones de navegacion
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("⏮ Primera", use_container_width=True):
                    st.session_state.pagina_clientes = 1
                    st.rerun()
            
            with col_btn2:
                if st.button("◀ Anterior", use_container_width=True):
                    if st.session_state.pagina_clientes > 1:
                        st.session_state.pagina_clientes -= 1
                        st.rerun()
            
            with col_btn3:
                if st.button("Siguiente ▶", use_container_width=True):
                    if st.session_state.pagina_clientes < total_paginas:
                        st.session_state.pagina_clientes += 1
                        st.rerun()
            
            with col_btn4:
                if st.button("⏭ Ultima", use_container_width=True):
                    st.session_state.pagina_clientes = total_paginas
                    st.rerun()
        
        with col_pag3:
            # Informacion de paginacion
            start_idx = (st.session_state.pagina_clientes - 1) * items_por_pagina + 1
            end_idx = min(start_idx + items_por_pagina - 1, total_clientes)
            st.markdown(f"""
            <div style="text-align: right; padding: 0.5rem;">
                <span style="color: #60a5fa;">Mostrando {start_idx} - {end_idx}</span>
                <span style="color: #6b7280;"> de {total_clientes} registros</span>
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== RESUMEN DE PAGINACION ====================
    st.markdown("---")
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d3f); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="color: #9ca3af;">Total Registros</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #fbbf24;">{total_clientes:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_res2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d3f); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="color: #9ca3af;">Paginas</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #60a5fa;">{total_paginas}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_res3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1e2e, #2d2d3f); border-radius: 12px; padding: 0.8rem; text-align: center;">
            <div style="color: #9ca3af;">Por Pagina</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #a78bfa;">{items_por_pagina}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== ACCIONES POR CLIENTE ====================
    st.divider()
    st.markdown("### ⚡ Acciones por Cliente")
    
    col_acc1, col_acc2 = st.columns(2)
    
    with col_acc1:
        if not clientes_df.empty and 'nombre' in clientes_df.columns:
            cliente_seleccionado = st.selectbox(
                "Seleccionar cliente:",
                clientes_df['nombre'].tolist()
            )
            
            if st.button(" Ver Detalles", use_container_width=True):
                cliente_data = clientes_df[clientes_df['nombre'] == cliente_seleccionado].iloc[0]
                st.markdown(f"""
                <div class="info-box">
                    <strong>📋 Informacion del Cliente</strong><br><br>
                    <strong>Nombre:</strong> {cliente_data.get('nombre', 'N/A')}<br>
                    <strong>Email:</strong> {cliente_data.get('email', 'N/A')}<br>
                    <strong>Telefono:</strong> {cliente_data.get('telefono', 'N/A')}<br>
                    <strong>Direccion:</strong> {cliente_data.get('direccion', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
    
    with col_acc2:
        st.markdown("### 📊 Estadisticas del Cliente")
        if not facturas_df.empty and 'Idcliente' in facturas_df.columns:
            top_clientes = facturas_df.groupby('Idcliente').size().sort_values(ascending=False).head(5)
            st.write(f"**Top 5 clientes por frecuencia:**")
            for idx, (cliente_id, count) in enumerate(top_clientes.items(), 1):
                st.write(f"{idx}. Cliente ID {cliente_id}: {count} compras")
        else:
            st.info("No hay datos de facturas para mostrar estadisticas")

else:
    st.info("No hay datos de clientes disponibles")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;"> Gestion de Clientes - Ferreteria IA</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Sistema Inteligente de Gestion Empresarial | Paginacion Integrada
    </p>
</div>
""", unsafe_allow_html=True)