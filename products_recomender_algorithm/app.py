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

st.title("🛍️ Catálogo Interactivo Carrusel")

# ----------------- FUNCION PARA MOSTRAR FILA DE PRODUCTOS -----------------
def mostrar_productos(productos, num_cols=5, prefijo="prod"):
    cols = st.columns(num_cols)
    for idx, producto in productos.iterrows():
        col_idx = idx % num_cols
        with cols[col_idx]:
            st.markdown(f"**{producto['name']}**")
            st.markdown(f"Marca: {producto['brand']}")
            st.markdown(f"Precio: ${producto['price']:.2f}")
            if st.button(f"Seleccionar {producto['name']}", key=f"{prefijo}_{producto['id']}"):
                st.session_state["producto_seleccionado"] = producto['id']

# ----------------- FUNCION PARA CAMBIAR OFFSET DE PRODUCTOS -----------------
def actualizar_offset(movimiento):
    st.session_state["producto_offset"] += movimiento
    if st.session_state["producto_offset"] < 0:
        st.session_state["producto_offset"] = 0
    if st.session_state["producto_offset"] >= len(df) - 5:  # Evitar ir más allá del total de productos
        st.session_state["producto_offset"] = len(df) - 5

# ----------------- BOTONES PARA DESPLAZAR CARRUSEL -----------------
columna_izquierda, columna_derecha = st.columns([1, 1])
with columna_izquierda:
    if st.button("◀️ Anterior"):
        actualizar_offset(-5)
with columna_derecha:
    if st.button("Siguiente ▶️"):
        actualizar_offset(5)

# ----------------- MOSTRAR PRODUCTOS SEGÚN OFFSET -----------------
productos_mostrar = df.iloc[st.session_state["producto_offset"]: st.session_state["producto_offset"] + 5]
mostrar_productos(productos_mostrar, num_cols=5, prefijo="all")

# ----------------- PRODUCTO SELECCIONADO -----------------
if st.session_state["producto_seleccionado"] is not None:
    idx_sel = df[df["id"] == st.session_state["producto_seleccionado"]].index[0]
    seleccionado = df.iloc[idx_sel]

    st.subheader("📌 Producto seleccionado")
    st.write(f"**{seleccionado['name']}**")
    st.write(f"Marca: {seleccionado['brand']}")
    st.write(f"Precio: ${seleccionado['price']:.2f}")
    st.write(f"Descripción: {seleccionado['description'] if isinstance(seleccionado['description'], str) else 'Sin descripción'}")

    # ----------------- RECOMENDACIONES -----------------
    recomendaciones = recomendar(idx_sel, top_n=5)
    st.subheader("✨ Productos relacionados")
    mostrar_productos(recomendaciones, num_cols=5, prefijo="rec")
