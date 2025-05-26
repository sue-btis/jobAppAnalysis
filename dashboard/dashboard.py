import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Seguimiento de Vacantes", layout="wide")

st.title("📊 Seguimiento de Aplicaciones Laborales")
st.markdown("Este panel muestra un resumen de correos relacionados con tus postulaciones.")

# Cargar datos
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["date"] = df["date"].dt.tz_localize(None)
    return df

try:
    df = load_data("data/tracker.csv")
except FileNotFoundError:
    st.warning("No se encontró el archivo tracker.csv. Ejecuta primero main.py.")
    st.stop()

# FILTROS SIDEBAR
with st.sidebar:
    st.header("🔍 Filtros")
    keyword = st.text_input("Filtrar por palabra clave (en asunto/cuerpo)")
    remitente = st.multiselect("Remitente", options=sorted(df["from"].unique()))
    estado = st.multiselect("Estado", options=sorted(df["estado"].unique()))
    fecha = st.date_input("Desde fecha", df["date"].min())

# Aplicar filtros
filtered_df = df.copy()

if keyword:
    keyword = keyword.lower()
    filtered_df = filtered_df[
        filtered_df["subject"].str.lower().str.contains(keyword) |
        filtered_df["snippet"].str.lower().str.contains(keyword)
    ]

if remitente:
    filtered_df = filtered_df[filtered_df["from"].isin(remitente)]

if estado:
    filtered_df = filtered_df[filtered_df["estado"].isin(estado)]

filtered_df = filtered_df[filtered_df["date"] >= pd.to_datetime(fecha)]

# Mostrar tabla
st.subheader(f"📬 Correos encontrados: {len(filtered_df)}")
st.dataframe(filtered_df, use_container_width=True)

# Gráfico: Correos por estado
st.subheader("📈 Estado del Proceso")
estado_count = filtered_df["estado"].value_counts().reset_index()
estado_count.columns = ["Estado", "Cantidad"]
fig_estado = px.bar(estado_count, x="Estado", y="Cantidad", title="Cantidad de correos por Estado")
st.plotly_chart(fig_estado, use_container_width=True)

# Gráfico temporal
st.subheader("📆 Actividad en el tiempo")
count_by_day = filtered_df.groupby(filtered_df["date"].dt.date).size().reset_index(name="Cantidad")
fig_tiempo = px.line(count_by_day, x="date", y="Cantidad", title="Correos por Día")
st.plotly_chart(fig_tiempo, use_container_width=True)
