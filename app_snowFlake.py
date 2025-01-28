import streamlit as st
import pandas as pd

# Configuración básica de la app
st.title("Análisis Rápido de Datasets")
st.write("Sube un archivo CSV, JSON o Excel para explorar su contenido.")

# Subir archivo
uploaded_file = st.file_uploader("Sube tu archivo aquí", type=["csv", "json", "xlsx"])

if uploaded_file is not None:
    # Detectar el formato del archivo
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        data = pd.read_json(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        data = pd.read_excel(uploaded_file)
    else:
        st.error("Formato no compatible.")

    # Mostrar información general
    st.subheader("Vista previa del dataset")
    st.dataframe(data.head())

    st.subheader("Información general")
    st.write(f"**Filas:** {data.shape[0]}")
    st.write(f"**Columnas:** {data.shape[1]}")

    st.subheader("Columnas y tipos de datos")
    st.write(data.dtypes)

    st.subheader("Datos faltantes por columna")
    st.write(data.isnull().sum())

    # Analizar categorías por columna
    st.subheader("Categorías por columna (si aplica)")
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        for col in categorical_cols:
            st.write(f"**{col}:** {data[col].nunique()} categorías")
            st.write(data[col].value_counts())
    else:
        st.write("No se detectaron columnas categóricas.")

    # Generar estadísticas básicas
    st.subheader("Estadísticas descriptivas")
    st.write(data.describe())

else:
    st.info("Por favor, sube un archivo para comenzar.")
