import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from database.models import obtener_facturas
from ml.predictor import predictor

st.set_page_config(page_title="Predicciones IA - Ferreteria IA", page_icon="", layout="wide")

st.title("Modelo Predictivo IA")
st.markdown("Predicciones basadas en inteligencia artificial")

facturas_df = obtener_facturas()

# Verificar datos
if not facturas_df.empty:
    st.info(f"Datos cargados: {len(facturas_df)} facturas disponibles")
    
    if 'Total' in facturas_df.columns:
        st.metric("Total de ventas registradas", f"C$ {facturas_df['Total'].sum():,.2f}")
    else:
        st.warning("La tabla de facturas no tiene la columna 'Total'")
else:
    st.warning("No hay datos de facturas disponibles")

if not facturas_df.empty and 'Total' in facturas_df.columns:
    
    # Entrenar modelo con manejo de errores
    with st.spinner("Preparando modelo predictivo..."):
        try:
            exito = predictor.entrenar_modelo(facturas_df)
            if exito:
                st.success("Modelo entrenado correctamente")
            else:
                st.info("Usando modelo basico (sin entrenamiento profundo)")
        except Exception as e:
            st.warning(f"Modelo en modo basico: {str(e)[:100]}")
    
    # Predicciones
    st.divider()
    dias_prediccion = st.slider("Dias a predecir:", 3, 30, 7)
    
    if st.button("Generar Predicciones", use_container_width=True):
        with st.spinner("IA generando predicciones..."):
            try:
                predicciones = predictor.predecir_ventas(facturas_df, dias_prediccion)
                
                # Grafico
                fig = go.Figure()
                
                # Datos historicos (ultimos 30 dias)
                datos_hist = facturas_df['Total'].tail(30)
                fig.add_trace(go.Scatter(
                    x=list(range(len(datos_hist))),
                    y=datos_hist.values,
                    mode='lines+markers',
                    name='Ventas Historicas',
                    line=dict(color='#3b82f6', width=2),
                    marker=dict(size=6)
                ))
                
                # Predicciones
                fig.add_trace(go.Scatter(
                    x=list(range(len(datos_hist), len(datos_hist) + dias_prediccion)),
                    y=predicciones,
                    mode='lines+markers',
                    name='Predicciones IA',
                    line=dict(color='#ef4444', width=2, dash='dash'),
                    marker=dict(size=6, symbol='diamond')
                ))
                
                fig.update_layout(
                    title="Prediccion de Ventas",
                    xaxis_title="Periodo",
                    yaxis_title="Ventas (C$)",
                    template="plotly_dark",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar predicciones en columnas
                st.subheader("Predicciones Detalladas")
                cols = st.columns(min(dias_prediccion, 5))
                for i, (col, pred) in enumerate(zip(cols, predicciones[:5])):
                    with col:
                        st.metric(f"Dia {i+1}", f"C$ {pred:,.2f}")
                
                # Mostrar todas las predicciones
                with st.expander("Ver todas las predicciones"):
                    for i, pred in enumerate(predicciones, 1):
                        st.write(f"Dia {i}: C$ {pred:,.2f}")
                        
            except Exception as e:
                st.error(f"Error generando predicciones: {str(e)}")
                st.info("Usando datos de ejemplo para demostracion")
                
                # Datos de ejemplo para demostracion
                predicciones_ejemplo = [120, 135, 150, 140, 160, 175, 190][:dias_prediccion]
                st.line_chart(predicciones_ejemplo, use_container_width=True)
    
    # Productos populares
    st.divider()
    st.subheader("Analisis de Productos")
    
    if st.button("Analizar Productos Populares", use_container_width=True):
        with st.spinner("Analizando productos..."):
            try:
                productos_populares = predictor.predecir_productos_populares(facturas_df)
                if isinstance(productos_populares, pd.DataFrame) and not productos_populares.empty:
                    st.dataframe(productos_populares, use_container_width=True)
                else:
                    st.info("Datos de productos de ejemplo")
                    df_ejemplo = pd.DataFrame({
                        'Producto': ['Martillo', 'Taladro', 'Sierra', 'Llaves', 'Pintura'],
                        'Ventas Estimadas': [125, 98, 76, 65, 52]
                    })
                    st.dataframe(df_ejemplo, use_container_width=True)
            except Exception as e:
                st.info("Datos de productos de ejemplo")
                df_ejemplo = pd.DataFrame({
                    'Producto': ['Martillo', 'Taladro', 'Sierra', 'Llaves', 'Pintura'],
                    'Ventas Estimadas': [125, 98, 76, 65, 52]
                })
                st.dataframe(df_ejemplo, use_container_width=True)
else:
    st.warning("No hay suficientes datos para generar predicciones")
    st.info("""
    **Se necesitan datos de ventas para el modelo predictivo.**
    
    Mientras tanto, puedes ver una demostracion:
    """)
    
    if st.button("Ver Demostracion del Modelo"):
        # Datos de ejemplo
        datos_ejemplo = [100, 120, 115, 130, 125, 140, 135, 150, 145, 160]
        st.line_chart(datos_ejemplo, use_container_width=True)
        st.success("El modelo predictivo comenzara a funcionar cuando haya datos reales de ventas")