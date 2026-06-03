import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote

from database.models import (
    obtener_inventario,
    obtener_proveedores,
    obtener_proveedor_producto
)

st.set_page_config(
    page_title="IA Agéntica - Ferretería IA",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.whatsapp-btn{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
    padding:16px;
    background:linear-gradient(135deg,#25D366,#128C7E);
    color:white !important;
    border-radius:16px;
    text-decoration:none !important;
    font-size:18px;
    font-weight:700;
    box-shadow:0 8px 25px rgba(37,211,102,.35);
    transition:all .3s ease;
}

.whatsapp-btn:hover{
    transform:translateY(-3px);
    box-shadow:0 12px 30px rgba(37,211,102,.55);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #070710 0%, #111827 45%, #1e1b4b 100%);
}

.main-header {
    background: linear-gradient(135deg, rgba(30,30,46,0.95), rgba(45,45,63,0.95));
    border-radius: 24px;
    padding: 2.2rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(96, 165, 250, 0.35);
    box-shadow: 0 15px 35px rgba(0,0,0,0.35);
}

.main-header h1 {
    color: #60a5fa;
    font-size: 2.6rem;
    margin-bottom: .4rem;
}

.main-header p {
    color: #cbd5e1;
    font-size: 1rem;
}

.badge-success {
    background: linear-gradient(135deg, #059669, #047857);
    color: white;
    padding: .4rem 1.2rem;
    border-radius: 30px;
    display: inline-block;
    font-weight: 600;
}

.order-card {
    background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
    border-radius: 18px;
    padding: 1.3rem;
    border: 1px solid rgba(96,165,250,.25);
    margin-bottom: 1rem;
}

.whatsapp-box {
    background: linear-gradient(135deg, rgba(5,150,105,.18), rgba(4,120,87,.18));
    border: 1px solid rgba(16,185,129,.45);
    border-radius: 16px;
    padding: 1rem;
    margin-top: 1rem;
}

.stButton button {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: none;
    border-radius: 14px;
    padding: .7rem 1rem;
    font-weight: 700;
    width: 100%;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(59,130,246,.4);
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
    border-radius: 18px;
    padding: 1rem;
    border: 1px solid rgba(96,165,250,.25);
}

.footer {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #1e1e2e, #2d2d3f);
    border-radius: 18px;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-header">
    <h1>🤖 IA Agéntica</h1>
    <p>Agente autónomo para monitoreo de stock, pedidos automáticos y envío por WhatsApp</p>
    <span class="badge-success">Sistema Autónomo Activo</span>
</div>
""", unsafe_allow_html=True)


inventario_df = obtener_inventario()
proveedores_df = obtener_proveedores()


def limpiar_telefono_whatsapp(telefono):
    if telefono is None:
        return ""

    telefono = str(telefono)
    telefono = telefono.replace(" ", "")
    telefono = telefono.replace("-", "")
    telefono = telefono.replace("+", "")
    telefono = telefono.replace("(", "")
    telefono = telefono.replace(")", "")

    if telefono.startswith("505"):
        return telefono

    if len(telefono) == 8:
        return "505" + telefono

    return telefono


def crear_link_whatsapp(telefono, mensaje):
    telefono_limpio = limpiar_telefono_whatsapp(telefono)

    if not telefono_limpio:
        return ""

    return f"https://wa.me/{telefono_limpio}?text={quote(mensaje)}"


class AgenteInteligente:
    def __init__(self, inventario, proveedores):
        self.inventario = inventario
        self.proveedores = proveedores
        self.tareas = []

    def obtener_proveedor_default(self):
        if self.proveedores.empty:
            return {
                "id": "N/A",
                "nombre": "Proveedor no definido",
                "telefono": ""
            }

        proveedor = self.proveedores.iloc[0]

        return {
            "id": proveedor["Idproveedor"] if "Idproveedor" in proveedor.index else "N/A",
            "nombre": proveedor["Razon_social"] if "Razon_social" in proveedor.index else "Proveedor",
            "telefono": proveedor["Telefono"] if "Telefono" in proveedor.index else ""
        }

    def obtener_proveedor_por_producto(self, idproducto):
        proveedor_df = obtener_proveedor_producto(idproducto)

        if proveedor_df.empty:
            return self.obtener_proveedor_default()

        proveedor = proveedor_df.iloc[0]

        return {
            "id": proveedor["Idproveedor"] if "Idproveedor" in proveedor.index else "N/A",
            "nombre": proveedor["Razon_social"] if "Razon_social" in proveedor.index else "Proveedor",
            "telefono": proveedor["Telefono"] if "Telefono" in proveedor.index else "",
            "correo": proveedor["Correo"] if "Correo" in proveedor.index else ""
        }

    def monitorear_stock(self):
        alertas = []

        if self.inventario.empty:
            return alertas

        if "Cantidad" not in self.inventario.columns:
            return alertas

        for idx, prod in self.inventario.iterrows():
            idproducto = prod["Idproducto"] if "Idproducto" in prod.index else None
            nombre = prod["Nombre"] if "Nombre" in prod.index else f"Producto {idx}"
            stock_actual = float(prod["Cantidad"])
            minimo = float(prod["Min_stock"]) if "Min_stock" in prod.index else 10

            if stock_actual <= minimo:
                alertas.append({
                    "idproducto": idproducto,
                    "producto": nombre,
                    "stock_actual": stock_actual,
                    "minimo": minimo
                })

        return alertas

    def redactar_mensaje_whatsapp(self, pedido):
        return (
            f"Hola, buen día estimado proveedor {pedido['proveedor_nombre']}.\n\n"
            f"Le saluda Ferretería Hodgson Luna.\n\n"
            f"Nuestro agente inteligente detectó que necesitamos realizar el siguiente pedido:\n\n"
            f"📦 Orden: {pedido['numero_orden']}\n"
            f"🛒 Producto: {pedido['producto']}\n"
            f"📊 Stock actual: {pedido['stock_actual']:.0f} unidades\n"
            f"⚠️ Stock mínimo: {pedido['stock_minimo']:.0f} unidades\n"
            f"✅ Cantidad solicitada: {pedido['cantidad']:.0f} unidades\n"
            f"📅 Fecha de solicitud: {pedido['fecha'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Por favor confirmar disponibilidad, precio actualizado y tiempo estimado de entrega.\n\n"
            f"Muchas gracias."
        )

    def procesar_pedido(self, alerta):
        proveedor = self.obtener_proveedor_por_producto(alerta["idproducto"])

        cantidad_pedido = max(alerta["minimo"] * 2, 1)

        pedido = {
            "idproducto": alerta["idproducto"],
            "producto": alerta["producto"],
            "stock_actual": alerta["stock_actual"],
            "stock_minimo": alerta["minimo"],
            "cantidad": cantidad_pedido,
            "proveedor_id": proveedor["id"],
            "proveedor_nombre": proveedor["nombre"],
            "proveedor_telefono": proveedor["telefono"],
            "fecha": datetime.now(),
            "estado": "Procesado por Agente IA",
            "numero_orden": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }

        pedido["mensaje_whatsapp"] = self.redactar_mensaje_whatsapp(pedido)
        pedido["link_whatsapp"] = crear_link_whatsapp(
            pedido["proveedor_telefono"],
            pedido["mensaje_whatsapp"]
        )

        self.tareas.append(pedido)
        return pedido

    def ejecutar(self):
        alertas = self.monitorear_stock()
        resultados = []

        for alerta in alertas[:5]:
            pedido = self.procesar_pedido(alerta)
            resultados.append(pedido)

        return {
            "alertas": len(alertas),
            "pedidos": len(resultados),
            "detalles": resultados
        }


agente = AgenteInteligente(inventario_df, proveedores_df)


with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem;">🤖</div>
        <h2 style="color: #60a5fa;">Agente IA</h2>
        <p style="color: #9ca3af;">Versión 2.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.success("Agente activo")

    st.markdown("""
    ### Capacidades
    - Monitoreo de stock
    - Pedidos automáticos
    - Selección de proveedor
    - Mensaje profesional
    - Enlace directo a WhatsApp
    """)

    st.markdown("---")
    st.caption(f"Última ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Productos", len(inventario_df) if not inventario_df.empty else 0)

with col2:
    if not inventario_df.empty and "Cantidad" in inventario_df.columns:
        if "Min_stock" in inventario_df.columns:
            stock_bajo = len(inventario_df[inventario_df["Cantidad"] <= inventario_df["Min_stock"]])
        else:
            stock_bajo = len(inventario_df[inventario_df["Cantidad"] <= 10])
        st.metric("Stock Crítico", stock_bajo)
    else:
        st.metric("Stock Crítico", 0)

with col3:
    st.metric("Proveedores", len(proveedores_df) if not proveedores_df.empty else 0)


st.divider()

st.markdown("## 🚀 Ejecución del Agente")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    ejecutar = st.button("🤖 Ejecutar Agente Inteligente", use_container_width=True)

if ejecutar:
    with st.spinner("El agente está analizando inventario, proveedores y pedidos..."):
        resultado = agente.ejecutar()
        st.session_state["ultimo_resultado_agente"] = resultado

if "ultimo_resultado_agente" in st.session_state:
    resultado = st.session_state["ultimo_resultado_agente"]

    st.success("✅ Agente completado exitosamente")

    col_r1, col_r2, col_r3 = st.columns(3)

    with col_r1:
        st.metric("Alertas Detectadas", resultado["alertas"])

    with col_r2:
        st.metric("Pedidos Generados", resultado["pedidos"])

    with col_r3:
        st.metric("WhatsApps Listos", resultado["pedidos"])

    if resultado["detalles"]:
        st.markdown("## 📦 Pedidos Automáticos Generados")

        for pedido in resultado["detalles"]:
            with st.expander(f"📦 Pedido: {pedido['producto']}"):
                st.markdown('<div class="order-card">', unsafe_allow_html=True)

                c1, c2 = st.columns(2)

                with c1:
                    st.write(f"**Producto:** {pedido['producto']}")
                    st.write(f"**Cantidad:** {pedido['cantidad']:.0f} unidades")
                    st.write(f"**Stock actual:** {pedido['stock_actual']:.0f}")
                    st.write(f"**Stock mínimo:** {pedido['stock_minimo']:.0f}")

                with c2:
                    st.write(f"**Orden:** {pedido['numero_orden']}")
                    st.write(f"**Proveedor:** {pedido['proveedor_nombre']}")
                    st.write(f"**Teléfono:** {pedido['proveedor_telefono']}")
                    st.write(f"**Estado:** {pedido['estado']}")

                st.write(f"**Fecha:** {pedido['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("### 🟢 Mensaje generado para WhatsApp")
                st.text_area(
                    "Mensaje",
                    value=pedido["mensaje_whatsapp"],
                    height=220,
                    key=f"msg_{pedido['numero_orden']}_{pedido['idproducto']}"
                )

                if pedido["link_whatsapp"]:
                    st.markdown(f"""
<a href="{pedido['link_whatsapp']}"
target="_blank"
class="whatsapp-btn">
📲 WhatsApp • Enviar Pedido al Proveedor
</a>
""", unsafe_allow_html=True)
                else:
                    st.warning("Este proveedor no tiene teléfono registrado para WhatsApp.")
    else:
        st.info("No se generaron pedidos. Todos los niveles de stock están normales.")


st.divider()

st.markdown("## 📊 Monitoreo en Tiempo Real")

col_m1, col_m2 = st.columns([1, 1])

with col_m1:
    st.markdown("### Estado actual del stock")

    if st.button("🔄 Actualizar Monitoreo", use_container_width=True):
        alertas = agente.monitorear_stock()

        if alertas:
            st.warning(f"Se detectaron {len(alertas)} productos con stock crítico.")

            for alerta in alertas[:10]:
                st.write(
                    f"- **{alerta['producto']}**: "
                    f"Stock {alerta['stock_actual']:.0f} "
                    f"(Mínimo {alerta['minimo']:.0f})"
                )
        else:
            st.success("Todos los niveles de stock son normales.")

with col_m2:
    st.markdown("### Rendimiento del agente")
    st.markdown(f"""
    <div class="whatsapp-box">
        <strong>📈 Estado operativo:</strong><br>
        - Monitoreo activo<br>
        - Pedidos automáticos habilitados<br>
        - WhatsApp generado por proveedor<br>
        - Tareas en memoria: {len(agente.tareas)}
    </div>
    """, unsafe_allow_html=True)


st.divider()

with st.expander("📋 Ver Datos del Sistema"):
    tab1, tab2 = st.tabs(["Inventario", "Proveedores"])

    with tab1:
        if not inventario_df.empty:
            st.dataframe(inventario_df, use_container_width=True)
        else:
            st.info("No hay datos de inventario disponibles.")

    with tab2:
        if not proveedores_df.empty:
            st.dataframe(proveedores_df, use_container_width=True)
        else:
            st.info("No hay datos de proveedores disponibles.")


st.markdown("""
<div class="footer">
    <p style="color: #60a5fa;">🤖 IA Agéntica - Agente Inteligente Autónomo</p>
    <p style="color: #6b7280; font-size: 0.8rem;">
        Monitoreo automático | Pedidos inteligentes | WhatsApp para proveedores
    </p>
</div>
""", unsafe_allow_html=True)