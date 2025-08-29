import pandas as pd
import numpy as np
from numpy.linalg import norm
df = pd.read_csv("data/dataset.csv")

categorias = df["category"]
marca = df["brand"]
price = df["price"]


#Vectorizando las categorias  las marcas
categorias_onehot= pd.get_dummies(categorias)
marcas_onehot = pd.get_dummies(marca)

#normalizo los precios
price_normalize = (df["price"] - df["price"].min()) / (df["price"].max() - df["price"].min())

#Creo la matriz
X = pd.concat([categorias_onehot, marcas_onehot, price_normalize], axis = 1)
X = X.to_numpy()

#funcion para calcular coseno
def similitud_coseno(vector_a , vector_b):
    return np.dot(vector_a, vector_b) / (norm(vector_a) * norm(vector_b))


#funcion para recomendar
def recomendar_producto(producto_index, X, top_n = 5):
    vector_ref = X[producto_index]
    similitudes = []


    for i in range(len(X)):
        if i != producto_index:
            simil = similitud_coseno(vector_ref,X[i])
            similitudes.append((i, simil))

    similitudes.sort(key = lambda x: x[1], reverse = True)


    recomendados = [i for i, _ in similitudes[:top_n]]
    return recomendados

#Funcion para ingresar datos, maneja los ingresos invalidos
def ingresar_id():
    while True:
        try:
            producto_id = int(input("Ingresa el id numerico del producto: "))
            
            # Verificar si el id existe en la columna 'id' del DataFrame
            if producto_id in df['id'].values:
                return producto_id  # Si el id es válido, lo devuelve
            else:
                print(f"Error: El id {producto_id} no existe. Por favor, ingrese un id válido.")
        except ValueError:
            print("Valor invalido, asegurese de ingresar un numero.")

#Muestro todos los productos
productos_seleccion = df[["id","name"]]
print("Los productos son: ")
print(f"{productos_seleccion}")


producto_id = ingresar_id()

producto_index = df.index[df["id"] == producto_id].tolist()[0]

recomendados = recomendar_producto(producto_index, X , top_n = 5)

print("Producto seleccionado: ")
print(df.loc[producto_index])

print("\nProductos recomendados:")
print(df.iloc[recomendados])
    

    