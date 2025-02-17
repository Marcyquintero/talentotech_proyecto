import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sc
import seaborn as sns
import plotly.express as px
from datetime import datetime
#1.
st.set_page_config(
  page_title="Dashboard Interactivo agroindustria",
  page_icon="",
  layout="wide"
)
st.title("Dashboard interactivo Agroindustria")
st.sidebar.title("Opciones de navegacion")

# 2. Generación de Datos Aleatorios
np.random.seed(150)
data = pd.DataFrame({
    "Fecha": pd.date_range(start="2024-01-01", periods=100, freq="D"),
    "Ventas": np.random.randint(100, 500, size=100),
    "Produccion_toneladas": np.random.randint(0,5000, size=100),
    "Tipo_produccion": np.random.choice(["Maiz", "Frijol", "Ahuyama", "Apio"], size=100),
    "Departamento": np.random.choice(["Antioquia", "Huila", "Cundinamarca", "Boyaca"], size=100),
    "Hectareas_sembradas": np.random.randint(0,5000, size=100),
    "Plagas_reportadas": np.random.randint(0,200, size=100),
    "Precio_venta": np.random.randint(0,200, size=100)
})

# 3. Implementación de la Barra de Navegación
menu = st.sidebar.radio(
    "Selecciona una opción:",
    ["Inicio", "Datos", "Visualización", "Configuración"]
)

# 4. Mostrar los Datos
if menu == "Datos":
    st.subheader("📂 Datos Generados")
    st.dataframe(data)
# 5. Filtrar por Categoría
filtered_data = data  # Asegurar que filtered_data esté definido en todo el script
if menu == "Visualización":
    st.subheader("📊 Visualización de Datos")
    categoria = st.sidebar.selectbox("Selecciona un departamento", data["Departamento"].unique())
    filtered_data = data[data["Departamento"] == categoria]
    st.write(f"Mostrando datos para Departamentos {categoria}")
    st.dataframe(filtered_data)

  # 6. Filtrar por Ventas
    ventas_min, ventas_max = st.sidebar.slider(
        "Selecciona el rango de ventas:",
        min_value=int(data["Ventas"].min()),
        max_value=int(data["Ventas"].max()),
        value=(int(data["Ventas"].min()), int(data["Ventas"].max()))
    )
    filtered_data = filtered_data[(filtered_data["Ventas"] >= ventas_min) & (filtered_data["Ventas"] <= ventas_max)]

  # 7. Filtrar por Fecha
    fecha_inicio, fecha_fin = st.sidebar.date_input(
        "Selecciona el rango de fechas:",
        [data["Fecha"].min(), data["Fecha"].max()],
        min_value=data["Fecha"].min(),
        max_value=data["Fecha"].max()
    )
    filtered_data = filtered_data[(filtered_data["Fecha"] >= pd.to_datetime(fecha_inicio)) & (filtered_data["Fecha"] <= pd.to_datetime(fecha_fin))]
   # 8. Botón para Reiniciar Filtros
    if st.sidebar.button("Reiniciar Filtros"):
        filtered_data = data
        st.experimental_rerun()

    # 9. Implementar Pestañas
    st.subheader("📌 Navegación entre Pestañas")
    tab1, tab2 = st.tabs(["📊 Gráficos", "📂 Datos"])
    with tab1:
        st.subheader("Visualización de Datos")
        fig_plotly = px.scatter(
            filtered_data,
            x="Departamento",
            y="Ventas",
            color="Tipo_produccion",
            title="Relación entre Ventas y Descuento por Departamento",
        )
        st.plotly_chart(fig_plotly)
    with tab2:
        st.subheader("Datos Crudos")
        st.dataframe(filtered_data)

# 10. Mensaje de Confirmación
st.sidebar.success("🎉 Configuración completa")

# 11. Ejecución del Script
if __name__ == "__main__":
    st.sidebar.info("Ejecuta este script con: streamlit run talento-roadmap-app.py")
