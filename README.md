Sistema de Recomendación de Productos

Este proyecto consiste en un sistema de recomendación de productos basado en similitudes entre categorías y marcas.
El objetivo es mostrar cómo funcionan los sistemas de recomendación de manera sencilla y práctica, integrando un frontend visual con Streamlit.

Funcionalidades

Carga de un dataset en formato CSV con productos.

Recomendaciones basadas en:

Categoría

Marca

Precio

Interfaz interactiva con Streamlit.

Posibilidad de explorar los productos recomendados con opción de "Ver más".

Estructura del Proyecto

app.py → Código principal de la aplicación

data/dataset.csv → Dataset de prueba con productos

README.md → Documentación del proyecto

Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado Python 3.9 o superior y las siguientes librerías:

pandas, numpy, streamlit

Se instalan con:

pip install pandas numpy streamlit

Ejecución

Clonar el repositorio o descargar los archivos.

Ubicar el dataset en la carpeta data/.

Ejecutar la aplicación con:

streamlit run app.py

Abrir el navegador en la dirección que aparece en la consola (por defecto: http://localhost:8501
).

Dataset de Ejemplo

El archivo dataset.csv debe contener al menos las siguientes columnas:

category: categoría del producto (ejemplo: "Electrónica")

brand: marca del producto

price: precio en valor numérico

Ejemplo de filas:

category,brand,price
Electrónica,Samsung,1200
Electrónica,Apple,2500
Ropa,Nike,150
Ropa,Adidas,130

Interfaz

La aplicación permite:

Seleccionar un producto base.

Ver los productos recomendados.

Expandir información de cada producto con el botón "Ver más".

Objetivo

Este proyecto está pensado como una demostración práctica para un portfolio.
Permite comprender cómo funcionan los sistemas de recomendación basados en similitud de atributos sin necesidad de usar algoritmos complejos.

Desarrollado por Rodrigo Nahuel Rosso
