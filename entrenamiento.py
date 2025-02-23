import pandas as pd
import streamlit as st
import plotly.express as px
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

# Configuración de la página de Streamlit
st.set_page_config(page_title="Visualización de Datos Climáticos", page_icon="", layout="wide")
st.title(" Visualización de Datos Climáticos")
st.sidebar.title(" Opciones de Navegación")

# Funciones de carga de datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_unificados (2).csv")

df_all = cargar_datos()

# Crear una nueva columna 'Fecha' combinando 'YEAR', 'MO', 'DY'
df_all['Fecha'] = pd.to_datetime(df_all.astype(str).loc[:, ["YEAR", "MO", "DY"]].agg('-'.join, axis=1))

# Función para crear mapas climáticos
def crear_mapa_clima(df, tipo_mapa, columna):
    max_row = df.loc[df[columna].idxmax()]
    map_center = [max_row["LAT"], max_row["LON"]]
    mapa = folium.Map(location=map_center, zoom_start=6)
    for _, row in df.iterrows():
        valor = row[columna]
        folium.CircleMarker(
            location=[row['LAT'], row['LON']],
            radius=valor * 0.1,
            color='green' if valor > df[columna].quantile(0.75) else 'orange' if valor > df[columna].quantile(0.5) else 'red',
            fill=True,
            fill_color='green' if valor > df[columna].quantile(0.75) else 'orange' if valor > df[columna].quantile(0.5) else 'red',
            fill_opacity=0.6,
            popup=f"{tipo_mapa}: {valor:.2f}"
        ).add_to(mapa)
    return mapa

# Menú de navegación en la barra lateral
menu = st.sidebar.selectbox("Selecciona una opción:", ["Inicio", "Datos", "Visualización", "Mapa Principal", "Análisis Detallado", "Matriz de Correlación", "Percentiles", "Mapas Climáticos", "Configuración"])

def get_region(lat, lon):
    if lat > 8: return "Caribe"
    elif lat < 2: return "Sur"
    elif lon < -75: return "Pacífico"
    return "Andina"

df_all['Region'] = df_all.apply(lambda x: get_region(x['LAT'], x['LON']), axis=1)

if menu == "Datos":
    st.subheader(" Datos Disponibles")
    st.dataframe(df_all)

elif menu == "Visualización":
    # ... (resto del código para la visualización)

elif menu == "Mapa Principal":
    # ... (resto del código para el mapa principal)

elif menu == "Análisis Detallado":
    # ... (resto del código para el análisis detallado)

elif menu == "Matriz de Correlación":
    st.subheader(" Matriz de Correlación de Variables Climáticas")
    df_corr = pd.read_csv("datos_unificados (2).csv") #Se usa el mismo archivo que en el resto del código
    df = df_corr.rename(columns={"RH2M": "Humedad relativa", "T2M": "Temperatura", "ALLSKY_SFC_SW_DWN": "Indice de claridad", "ALLSKY_KT": "Irradiancia solar", "PRECTOTCORR": "Precipitacion"})
    columnas_deseadas = ["Irradiancia solar", "Indice de claridad", "Temperatura", "Humedad relativa", "Precipitacion"]
    df_seleccionado = df[columnas_deseadas]
    matriz_correlacion = df_seleccionado.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Matriz de Correlación')
    st.pyplot(plt)

elif menu == "Configuración":
    st.sidebar.success(" Configuración completa")

elif menu == "Percentiles":
    # ... (resto del código para los percentiles)

elif menu == "Mapas Climáticos":
    st.subheader("️ Mapas de Humedad, Precipitación y Temperatura")
    tipo_mapa = st.selectbox("Selecciona el tipo de mapa:", ["Humedad", "Precipitación", "Temperatura"])
    if tipo_mapa == "Humedad":
        mapa = crear_mapa_clima(df_all, tipo_mapa, "RH2M")
    elif tipo_mapa == "Precipitación":
        mapa = crear_mapa_clima(df_all, tipo_mapa, "PRECTOTCORR")
    elif tipo_mapa == "Temperatura":
        mapa = crear_mapa_clima(df_all, tipo_mapa, "T2M")
    if mapa:
        st_folium(mapa, width=700, height=400)

if __name__ == "__main__":
    st.sidebar.info("Ejecuta este script con: streamlit run solaris_app.py.py")
