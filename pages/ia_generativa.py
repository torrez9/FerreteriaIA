import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database.models import obtener_facturas, obtener_inventario, obtener_productos, obtener_clientes

# Configuracion de la pagina
st.set_page_config(
    page_title="IA Generativa - Ferreteria IA", 
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
    
    .badge-ia {
        background: linear-gradient(135deg, #7c3aed, #6d28d9);
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
    
    /* === SELECTBOX === */
    .stSelectbox div {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.2);
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
    
    /* === CODE BLOCK === */
    .stCodeBlock {
        border-radius: 12px;
        background: linear-gradient(135deg, #1a1a2e, #0f0f1a);
        border: 1px solid rgba(96, 165, 250, 0.2);
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
    
    /* === GENERATION CARD === */
    .gen-card {
        background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
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

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1> IA Generativa</h1>
    <p>Generacion automatica de contenido empresarial con inteligencia artificial</p>
    <span class="badge-ia">Potenciado por IA Generativa</span>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
facturas_df = obtener_facturas()
inventario_df = obtener_inventario()
productos_df = obtener_productos()
clientes_df = obtener_clientes()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">✨</div>
        <h2 style="color: #60a5fa;">IA Generativa</h2>
        <p style="color: #9ca3af;">Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Capacidades de IA")
    st.markdown("""
    - 📊 Reportes de ventas
    - 📦 Resumen de inventario
    - ✉️ Correos promocionales
    - 📈 Analisis predictivo
    - 📄 Documentacion automatica
    """)
    
    st.markdown("---")
    
    st.markdown("### Estadisticas de Datos")
    if not facturas_df.empty:
        st.metric("Ventas Registradas", len(facturas_df))
    if not inventario_df.empty:
        st.metric("Productos en Stock", len(inventario_df))
    if not clientes_df.empty:
        st.metric("Clientes Activos", len(clientes_df))
    
    st.markdown("---")
    st.markdown(f"**Ultima generacion:**")
    st.caption(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# ==================== METRICAS CLAVE ====================
st.markdown("## Metricas del Sistema")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if not facturas_df.empty and 'Total' in facturas_df.columns:
        ventas_totales = facturas_df['Total'].sum()
        st.metric("Ingresos Totales", f"C$ {ventas_totales:,.2f}")
    else:
        st.metric("Ingresos Totales", "N/A")

with col2:
    if not facturas_df.empty:
        num_ventas = len(facturas_df)
        st.metric("Transacciones", f"{num_ventas:,}")
    else:
        st.metric("Transacciones", "N/A")

with col3:
    if not inventario_df.empty:
        total_productos = len(inventario_df)
        st.metric("Productos", f"{total_productos:,}")
    else:
        st.metric("Productos", "N/A")

with col4:
    if not clientes_df.empty:
        total_clientes = len(clientes_df)
        st.metric("Clientes", f"{total_clientes:,}")
    else:
        st.metric("Clientes", "N/A")

st.divider()

# ==================== FUNCIONES DE GENERACION MEJORADAS ====================

def generar_reporte_ventas_completo():
    """Genera reporte de ventas completo con analisis"""
    if facturas_df.empty:
        return "⚠️ No hay datos de ventas disponibles para generar el reporte."
    
    total_ventas = facturas_df['Total'].sum() if 'Total' in facturas_df.columns else 0
    num_ventas = len(facturas_df)
    promedio = total_ventas / num_ventas if num_ventas > 0 else 0
    
    # Calcular crecimiento estimado
    if len(facturas_df) > 10:
        ventas_recientes = facturas_df['Total'].tail(5).mean() if 'Total' in facturas_df.columns else 0
        ventas_anteriores = facturas_df['Total'].head(5).mean() if 'Total' in facturas_df.columns else 0
        crecimiento = ((ventas_recientes - ventas_anteriores) / ventas_anteriores * 100) if ventas_anteriores > 0 else 0
    else:
        crecimiento = 0
    
    reporte = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    REPORTE DE VENTAS - IA GENERATIVA              ║
╠══════════════════════════════════════════════════════════════════╣
║ Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║
╠══════════════════════════════════════════════════════════════════╣
║                          RESUMEN GENERAL                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  📊 Total de ventas:          {num_ventas:>10,} transacciones      ║
║  💰 Ingresos totales:         C$ {total_ventas:>12,.2f}            ║
║  🎫 Ticket promedio:          C$ {promedio:>12,.2f}            ║
║  📈 Crecimiento estimado:     {crecimiento:>10,.1f}%                ║
║                                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║                          ANALISIS DETALLADO                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  El negocio ha generado C$ {total_ventas:,.2f} en {num_ventas} transacciones.      ║
║  El ticket promedio de C$ {promedio:,.2f} se considera                               ║
║  {'ALTO' if promedio > 500 else 'MODERADO' if promedio > 200 else 'BAJO'}.                       ║
║                                                                   ║
║  {'📈 Tendencia positiva detectada' if crecimiento > 5 else '📉 Tendencia estable'}                          ║
║                                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║                        RECOMENDACIONES                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  ✅ {'Mantener estrategia actual y enfocar en retencion' if num_ventas > 100 else 'Implementar campañas de captacion'}     ║
║  ✅ {'Optimizar productos de alto valor' if promedio > 300 else 'Buscar aumentar ticket promedio'}                    ║
║  ✅ Revisar productos con mejor rendimiento                         ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
    """
    return reporte

def generar_resumen_inventario_completo():
    """Genera resumen completo del inventario"""
    if inventario_df.empty:
        return "⚠️ No hay datos de inventario disponibles"
    
    total = len(inventario_df)
    
    if 'Estado_Stock' in inventario_df.columns:
        stock_bajo = len(inventario_df[inventario_df['Estado_Stock'] == 'Bajo Stock'])
        stock_medio = len(inventario_df[inventario_df['Estado_Stock'] == 'Stock Medio'])
        stock_alto = len(inventario_df[inventario_df['Estado_Stock'] == 'Stock Alto'])
    else:
        stock_bajo = len(inventario_df[inventario_df['Cantidad'] <= 10]) if 'Cantidad' in inventario_df.columns else 0
        stock_medio = len(inventario_df[(inventario_df['Cantidad'] > 10) & (inventario_df['Cantidad'] <= 50)]) if 'Cantidad' in inventario_df.columns else 0
        stock_alto = len(inventario_df[inventario_df['Cantidad'] > 50]) if 'Cantidad' in inventario_df.columns else 0
    
    total_unidades = inventario_df['Cantidad'].sum() if 'Cantidad' in inventario_df.columns else 0
    
    resumen = f"""
╔══════════════════════════════════════════════════════════════════╗
║                   RESUMEN DE INVENTARIO - IA GENERATIVA           ║
╠══════════════════════════════════════════════════════════════════╣
║ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                          ESTADO GENERAL                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  📦 Total productos:         {total:>10,}                         ║
║  📊 Unidades en stock:       {total_unidades:>10,}                         ║
║                                                                   ║
║  DISTRIBUCION DE STOCK:                                           ║
║  🔴 Stock bajo:              {stock_bajo:>10,} ({stock_bajo/total*100:.1f}%)        ║
║  🟡 Stock medio:             {stock_medio:>10,} ({stock_medio/total*100:.1f}%)        ║
║  🟢 Stock alto:              {stock_alto:>10,} ({stock_alto/total*100:.1f}%)        ║
║                                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║                        ACCIONES RECOMENDADAS                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  {'🔴 URGENTE: Realizar pedidos para productos con stock bajo' if stock_bajo > 0 else '✅ Niveles de stock optimos'}        ║
║  📋 Revisar productos de alta rotacion semanalmente                ║
║  📊 Implementar sistema de alertas preventivas                    ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
    """
    return resumen

def generar_correo_promocional_personalizado():
    """Genera correo promocional personalizado con datos reales"""
    num_clientes = len(clientes_df) if not clientes_df.empty else 0
    total_productos = len(productos_df) if not productos_df.empty else 0
    
    correo = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    CORREO PROMOCIONAL - IA GENERATIVA             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Asunto: 🎉 OFERTA ESPECIAL para nuestros clientes                ║
║                                                                   ║
║  Estimado cliente,                                                ║
║                                                                   ║
║  Nuestro sistema de Inteligencia Artificial ha analizado         ║
║  tus preferencias y tenemos una oferta especial para ti.         ║
║                                                                   ║
║  🎯 PROMOCIONES DESTACADAS:                                       ║
║                                                                   ║
║  • 15% de descuento en herramientas profesionales                ║
║  • 2x1 en productos seleccionados                                ║
║  • Envío gratis en compras mayores a C$ 500                      ║
║                                                                   ║
║  📊 Datos de interes:                                             ║
║  • {num_clientes}+ clientes satisfechos                             ║
║  • {total_productos}+ productos disponibles                         ║
║  • Atencion personalizada 24/7                                   ║
║                                                                   ║
║  🔗 Usa el codigo: IAGENERATIVA2024                              ║
║                                                                   ║
║  ¡No dejes pasar esta oportunidad!                               ║
║                                                                   ║
║  Saludos cordiales,                                               ║
║  Equipo Ferreteria IA                                             ║
║  🤖 Potenciado por IA Generativa                                  ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
    """
    return correo

def generar_reporte_ejecutivo():
    """Genera reporte ejecutivo completo"""
    if facturas_df.empty:
        return "⚠️ No hay datos suficientes para generar el reporte ejecutivo"
    
    total_ventas = facturas_df['Total'].sum() if 'Total' in facturas_df.columns else 0
    num_ventas = len(facturas_df)
    promedio = total_ventas / num_ventas if num_ventas > 0 else 0
    
    total_productos = len(inventario_df) if not inventario_df.empty else 0
    total_clientes = len(clientes_df) if not clientes_df.empty else 0
    
    reporte = f"""
╔══════════════════════════════════════════════════════════════════╗
║                   REPORTE EJECUTIVO - FERRETERIA IA               ║
╠══════════════════════════════════════════════════════════════════╣
║ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  🏪 RESUMEN GENERAL DEL NEGOCIO                                   ║
║  ─────────────────────────────────────────────────────────────   ║
║                                                                   ║
║  INDICADORES CLAVE:                                               ║
║  • Clientes registrados: {total_clientes:>10,}                             ║
║  • Productos en catalogo: {total_productos:>10,}                             ║
║  • Transacciones realizadas: {num_ventas:>10,}                             ║
║  • Ingresos totales: C$ {total_ventas:>12,.2f}                    ║
║  • Ticket promedio: C$ {promedio:>12,.2f}                        ║
║                                                                   ║
║  📈 ANALISIS DE RENDIMIENTO                                       ║
║  ─────────────────────────────────────────────────────────────   ║
║                                                                   ║
║  El negocio presenta un rendimiento                              ║
║  {'EXCELENTE' if num_ventas > 200 else 'BUENO' if num_ventas > 100 else 'EN DESARROLLO'}.                                   ║
║  El ticket promedio de C$ {promedio:,.2f} se encuentra             ║
║  en nivel {'ALTO' if promedio > 500 else 'MEDIO' if promedio > 200 else 'BAJO'}.                                    ║
║                                                                   ║
║  🎯 RECOMENDACIONES ESTRATEGICAS                                  ║
║  ─────────────────────────────────────────────────────────────   ║
║                                                                   ║
║  1. {'Mantener estrategia actual' if num_ventas > 150 else 'Implementar campañas agresivas de marketing'}                    ║
║  2. {'Fidelizar clientes existentes' if promedio > 300 else 'Aumentar ticket promedio con upselling'}                 ║
║  3. Optimizar inventario segun demanda                          ║
║  4. Expandir presencia digital                                   ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
    """
    return reporte

# ==================== INTERFAZ PRINCIPAL ====================
st.markdown("## Generador de Contenido IA")

col_gen1, col_gen2 = st.columns([1, 2])

with col_gen1:
    st.markdown('<div class="card-title"> Selecciona el tipo de contenido</div>', unsafe_allow_html=True)
    
    tipo = st.selectbox(
        "Tipo de contenido a generar:",
        ["📊 Reporte de Ventas Completo", "📦 Resumen de Inventario", "✉️ Correo Promocional", "📈 Reporte Ejecutivo"]
    )
    
    st.markdown("---")
    st.markdown("### Personalizacion")
    
    incluir_fecha = st.checkbox("Incluir fecha detallada", value=True)
    formato_destacado = st.checkbox("Formato destacado", value=True)
    
    st.markdown("---")
    st.markdown("### Historial de Generaciones")
    st.caption("La IA recuerda tus preferencias")

with col_gen2:
    st.markdown('<div class="card-title"> Contenido Generado</div>', unsafe_allow_html=True)
    
    if st.button("✨ Generar Contenido con IA", use_container_width=True):
        with st.spinner("🧠 IA Generativa trabajando..."):
            if "Reporte de Ventas" in tipo:
                contenido = generar_reporte_ventas_completo()
            elif "Resumen de Inventario" in tipo:
                contenido = generar_resumen_inventario_completo()
            elif "Correo Promocional" in tipo:
                contenido = generar_correo_promocional_personalizado()
            else:
                contenido = generar_reporte_ejecutivo()
            
            # Mostrar contenido
            st.code(contenido, language="text")
            
            # Botones de accion
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.download_button(
                    "📥 Descargar Contenido",
                    contenido,
                    file_name=f"contenido_ia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True
                )
            with col_btn2:
                st.button("📋 Copiar al portapapeles", use_container_width=True)
            
            st.balloons()
            st.success("✅ Contenido generado exitosamente por IA Generativa")

# ==================== EJEMPLOS RAPIDOS ====================
st.divider()
st.markdown("## Ejemplos Rapidos")

col_ej1, col_ej2, col_ej3 = st.columns(3)

with col_ej1:
    if st.button("📊 Ver ejemplo de Reporte", use_container_width=True):
        with st.spinner("Generando ejemplo..."):
            st.code(generar_reporte_ventas_completo(), language="text")

with col_ej2:
    if st.button("📦 Ver ejemplo de Inventario", use_container_width=True):
        with st.spinner("Generando ejemplo..."):
            st.code(generar_resumen_inventario_completo(), language="text")

with col_ej3:
    if st.button("✉️ Ver ejemplo de Correo", use_container_width=True):
        with st.spinner("Generando ejemplo..."):
            st.code(generar_correo_promocional_personalizado(), language="text")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;">✨ IA Generativa - Ferreteria IA</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Reportes Automaticos | Resumenes Inteligentes | Contenido Personalizado
    </p>
    <p style="color: #4b5563; font-size: 0.7rem;">
        Potenciado por modelos de lenguaje avanzados
    </p>
</div>
""", unsafe_allow_html=True)