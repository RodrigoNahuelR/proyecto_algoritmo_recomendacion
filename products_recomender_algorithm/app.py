import streamlit as st
import pandas as pd
import numpy as np
from numpy.linalg import norm

# ----------------- CARGA DE DATOS -----------------
df = pd.read_csv("data/dataset.csv")

# Vectorización de categorías y marcas + normalización del precio
categorias_onehot = pd.get_dummies(df["category"])
marcas_onehot = pd.get_dummies(df["brand"])
features = pd.concat([categorias_onehot, marcas_onehot, df[["price"]]], axis=1)
features["price"] = (features["price"] - features["price"].min()) / (features["price"].max() - features["price"].min())

# ----------------- FUNCIONES -----------------
def similitud_coseno(vector_a, vector_b):
    return np.dot(vector_a, vector_b) / (norm(vector_a) * norm(vector_b))

def recomendar(producto_idx, top_n=5):
    vector_objetivo = features.iloc[producto_idx].values
    similitudes = features.apply(lambda row: similitud_coseno(row.values, vector_objetivo), axis=1)
    similares_idx = similitudes.sort_values(ascending=False).index[1:top_n+1]
    return df.iloc[similares_idx]

# ----------------- SESSION STATE -----------------
if "producto_seleccionado" not in st.session_state:
    st.session_state["producto_seleccionado"] = None
if "producto_offset" not in st.session_state:
    st.session_state["producto_offset"] = 0

# ----------------- HEADER -----------------
st.title("🛒 Sistema de Recomendación de Productos")
st.caption("Explora el catálogo, selecciona un producto y descubre artículos relacionados.")

# ----------------- FUNCIONES FRONTEND -----------------
def mostrar_producto_card(producto, key_prefix="prod"):
    """Muestra un producto en formato tarjeta con botón de selección"""
    with st.container():
        st.markdown(f"""
        <div style='border:1px solid #ddd; border-radius:10px; padding:10px; margin-bottom:10px;'>
            <h4>{producto['name']}</h4>
            <p><b>Marca:</b> {producto['brand']}<br>
            <b>Precio:</b> ${producto['price']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Ver más", key=f"{key_prefix}_{producto['id']}"):
            st.session_state["producto_seleccionado"] = producto['id']

def mostrar_productos(productos, num_cols=5, prefijo="prod"):
    """Muestra una fila de productos en columnas"""
    cols = st.columns(num_cols)
    for idx, producto in productos.iterrows():
        col_idx = idx % num_cols
        with cols[col_idx]:
            mostrar_producto_card(producto, key_prefix=prefijo)

def actualizar_offset(movimiento, page_size=5):
    """Mueve el offset del carrusel"""
    st.session_state["producto_offset"] += movimiento
    if st.session_state["producto_offset"] < 0:
        st.session_state["producto_offset"] = 0
    if st.session_state["producto_offset"] >= len(df) - page_size:
        st.session_state["producto_offset"] = len(df) - page_size

# ----------------- CARRUSEL -----------------
page_size = 5
total_pages = (len(df) // page_size) + 1

st.write("---")
col_prev, col_page, col_next = st.columns([1, 2, 1])
with col_prev:
    if st.button("◀️ Anterior"):
        actualizar_offset(-page_size, page_size)
with col_page:
    st.markdown(f"**Página {(st.session_state['producto_offset']//page_size)+1} de {total_pages}**")
with col_next:
    if st.button("Siguiente ▶️"):
        actualizar_offset(page_size, page_size)

productos_mostrar = df.iloc[
    st.session_state["producto_offset"]: st.session_state["producto_offset"] + page_size
]
mostrar_productos(productos_mostrar, num_cols=5, prefijo="all")

# ----------------- PRODUCTO SELECCIONADO -----------------
if st.session_state["producto_seleccionado"] is not None:
    idx_sel = df[df["id"] == st.session_state["producto_seleccionado"]].index[0]
    seleccionado = df.iloc[idx_sel]

    st.write("---")
    st.subheader("📌 Producto seleccionado")
    with st.container():
        st.markdown(f"""
        <div style='border:2px solid #4CAF50; border-radius:12px; padding:15px; margin-bottom:15px;'>
            <h3>{seleccionado['name']}</h3>
            <p><b>Marca:</b> {seleccionado['brand']}<br>
            <b>Precio:</b> ${seleccionado['price']:.2f}</p>
            <p><b>Descripción:</b> {seleccionado['description'] if isinstance(seleccionado['description'], str) else 'Sin descripción'}</p>
        </div>
        """, unsafe_allow_html=True)

    # ----------------- RECOMENDACIONES -----------------
    recomendaciones = recomendar(idx_sel, top_n=5)
    st.subheader("✨ Productos relacionados")
    mostrar_productos(recomendaciones, num_cols=5, prefijo="rec")
