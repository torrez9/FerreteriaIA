import streamlit as st
from datetime import datetime
from database.models import obtener_inventario, obtener_proveedores

st.set_page_config(page_title="IA Agentica - Ferreteria IA", page_icon="", layout="wide")

st.title("IA Agentica - Agente Inteligente Autonomo")
st.markdown("Agente que monitorea y ejecuta procesos automaticamente")

inventario_df = obtener_inventario()
proveedores_df = obtener_proveedores()

# Mostrar las columnas disponibles para debug (opcional, puedes eliminar después)
if not proveedores_df.empty:
    st.caption(f"Columnas disponibles en proveedores: {list(proveedores_df.columns)}")

class AgenteInteligente:
    def __init__(self, inventario, proveedores):
        self.inventario = inventario
        self.proveedores = proveedores
        self.tareas = []
    
    def obtener_nombre_proveedor(self):
        """Obtiene el nombre del proveedor de forma segura"""
        if self.proveedores.empty:
            return "Proveedor Default"
        
        # Intentar diferentes nombres de columna posibles
        posibles_columnas = ['nombre', 'Nombre', 'NOMBRE', 'nombre_proveedor', 'proveedor', 'Proveedor', 'name', 'Name']
        
        for col in posibles_columnas:
            if col in self.proveedores.columns:
                return str(self.proveedores.iloc[0][col])
        
        # Si no encuentra ninguna columna de nombre, retorna el primer valor como string
        return str(self.proveedores.iloc[0].iloc[0]) if len(self.proveedores.columns) > 0 else "Proveedor Default"
    
    def monitorear_stock(self):
        """Monitorea niveles de stock"""
        alertas = []
        if not self.inventario.empty:
            # Verificar que existan las columnas necesarias
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
                # Si no hay Min_stock, usar un minimo por defecto
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
            'estado': 'Procesado por Agente IA'
        }
        self.tareas.append(pedido)
        return pedido
    
    def ejecutar(self):
        """Ejecuta el ciclo del agente"""
        alertas = self.monitorear_stock()
        resultados = []
        
        for alerta in alertas[:3]:
            cantidad_pedido = alerta['minimo'] * 2
            pedido = self.procesar_pedido(alerta['producto'], cantidad_pedido)
            resultados.append(pedido)
        
        return {
            'alertas': len(alertas),
            'pedidos': len(resultados),
            'detalles': resultados
        }

# Crear instancia del agente
agente = AgenteInteligente(inventario_df, proveedores_df)

# Boton para ejecutar el agente
if st.button("Ejecutar Agente IA", use_container_width=True):
    with st.spinner("Agente inteligente analizando el sistema..."):
        resultado = agente.ejecutar()
        
        st.success(f"Agente completado - {resultado['alertas']} alertas, {resultado['pedidos']} pedidos")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Alertas Detectadas", resultado['alertas'])
        with col2:
            st.metric("Pedidos Procesados", resultado['pedidos'])
        
        if resultado['detalles']:
            st.subheader("Pedidos Automaticos Generados")
            for pedido in resultado['detalles']:
                with st.expander(f"Pedido: {pedido['producto']}"):
                    st.write(f"Cantidad: {pedido['cantidad']} unidades")
                    st.write(f"Proveedor: {pedido['proveedor']}")
                    st.write(f"Fecha: {pedido['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"Estado: {pedido['estado']}")

# Monitoreo continuo
st.divider()
st.subheader("Monitoreo en Tiempo Real")

if st.button("Actualizar Monitoreo"):
    alertas = agente.monitorear_stock()
    
    if alertas:
        st.warning(f"Se detectaron {len(alertas)} productos con stock critico")
        for alerta in alertas:
            st.write(f"- {alerta['producto']}: Stock {alerta['stock_actual']} (Minimo {alerta['minimo']})")
    else:
        st.success("Niveles de stock normales")

# Mostrar informacion de las tablas
st.divider()
with st.expander("Ver estructura de datos actual"):
    st.subheader("Inventario")
    if not inventario_df.empty:
        st.write(f"Columnas: {list(inventario_df.columns)}")
        st.dataframe(inventario_df.head(), use_container_width=True)
    else:
        st.info("No hay datos de inventario")
    
    st.subheader("Proveedores")
    if not proveedores_df.empty:
        st.write(f"Columnas: {list(proveedores_df.columns)}")
        st.dataframe(proveedores_df.head(), use_container_width=True)
    else:
        st.info("No hay datos de proveedores")