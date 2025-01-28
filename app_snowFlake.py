import streamlit as st
import pandas as pd

# Configuración de la app
st.set_page_config(page_title="Snowflake Table Catalog", layout="wide")

# Título
st.title("📊 Explorador de Datasets con Tarjetas")

# Sidebar
st.sidebar.header("Opciones de Filtro")
order_by = st.sidebar.selectbox("Ordenar por", ["A → Z", "Z → A", "Tamaño (Mayor a Menor)", "Tamaño (Menor a Mayor)"])
table_type = st.sidebar.multiselect("Tipo de Tabla", ["Base Table", "View"], default=["Base Table", "View"])
data_size_filter = st.sidebar.slider("Tamaño del Dataset (MB)", 0, 500, (0, 500))
rows_filter = st.sidebar.slider("Número de Filas", 0, 1000000, (0, 1000000))

# Subir archivo
uploaded_file = st.file_uploader("Sube tu archivo aquí (CSV, JSON, Excel)", type=["csv", "json", "xlsx"])

if uploaded_file is not None:
    # Leer el archivo
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.json'):
        data = pd.read_json(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        data = pd.read_excel(uploaded_file)
    
    # Calcular información del dataset
    data_size_mb = data.memory_usage(deep=True).sum() / (1024 * 1024)
    rows, cols = data.shape

    # Filtro por tamaño de datos y número de filas
    if not (data_size_filter[0] <= data_size_mb <= data_size_filter[1] and rows_filter[0] <= rows <= rows_filter[1]):
        st.warning("El dataset no cumple con los filtros seleccionados.")
    else:
        # Mostrar estadísticas del dataset en una tarjeta
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: #f9f9f9;">
            <h3 style="color: #4CAF50;">Dataset: {uploaded_file.name}</h3>
            <p><strong>Tamaño:</strong> {data_size_mb:.2f} MB</p>
            <p><strong>Filas:</strong> {rows}</p>
            <p><strong>Columnas:</strong> {cols}</p>
            <p><strong>Columnas categóricas:</strong> {len(data.select_dtypes(include=['object', 'category']).columns)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar tabla filtrada
        st.subheader("Vista previa del dataset")
        st.dataframe(data.head())

        # Mostrar estadísticas adicionales
        st.subheader("Información general del dataset")
        st.write(data.describe())

else:
    st.info("Sube un archivo para comenzar.")

# Mensaje final
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado con ❤️ por Streamlit")
