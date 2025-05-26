import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Seguimiento de Vacantes", layout="wide")

st.title("📊 Seguimiento de Aplicaciones Laborales")
st.markdown("Este panel muestra un resumen de correos relacionados con tus postulaciones y un análisis de tus aplicaciones registradas manualmente.")


@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["date"] = df["date"].dt.tz_localize(None)
    return df

def limpiar_remitente(remitente):
    match = re.search(r'<([^>]+)>', str(remitente))
    if match:
        return match.group(1).strip()
    else:
        return str(remitente).strip().strip('"')


# TABS

tab1, tab2 = st.tabs(["📬 Correos", "📂 Aplicaciones (CSV)"])


# TAB 1 - Correos

with tab1:
    try:
        df = load_data("data/tracker.csv")
    except FileNotFoundError:
        st.warning("No se encontró el archivo tracker.csv. Ejecuta primero main.py.")
        st.stop()

    # Limpieza de remitente
    df["empresa_limpia"] = df["from"].apply(limpiar_remitente)

    with st.sidebar:
        st.header("🔍 Filtros")
        keyword = st.text_input("Filtrar por palabra clave (en asunto/cuerpo)")
        remitente = st.multiselect("Remitente", options=sorted(df["empresa_limpia"].dropna().unique()))
        estado = st.multiselect("Estado", options=sorted(df["estado"].dropna().unique()))
        fecha = st.date_input("Desde fecha", df["date"].min())

    filtered_df = df.copy()

    if keyword:
        keyword = keyword.lower()
        filtered_df = filtered_df[
            filtered_df["subject"].str.lower().str.contains(keyword, na=False) |
            filtered_df["snippet"].str.lower().str.contains(keyword, na=False)
        ]

    if remitente:
        filtered_df = filtered_df[filtered_df["empresa_limpia"].isin(remitente)]

    if estado:
        filtered_df = filtered_df[filtered_df["estado"].isin(estado)]

    filtered_df = filtered_df[filtered_df["date"] >= pd.to_datetime(fecha)]

    st.subheader(f"📬 Correos encontrados: {len(filtered_df)}")
    st.dataframe(filtered_df, use_container_width=True)

    # Estado del proceso
    st.subheader("📈 Estado del Proceso")
    estado_count = filtered_df["estado"].value_counts().reset_index()
    estado_count.columns = ["Estado", "Cantidad"]
    fig_estado = px.bar(estado_count, x="Estado", y="Cantidad", title="Cantidad de correos por Estado")
    st.plotly_chart(fig_estado, use_container_width=True)

    # Aplicaciones por mes (línea de tiempo)
    filtered_df["mes"] = filtered_df["date"].dt.to_period("M").dt.to_timestamp()
    apps_por_mes = filtered_df.groupby("mes").size().reset_index(name="Aplicaciones")
    fig_mes = px.line(
        apps_por_mes,
        x="mes",
        y="Aplicaciones",
        markers=True,
        title="📈 Aplicaciones por Mes (Correos)"
    )
    st.plotly_chart(fig_mes, use_container_width=True)


    st.markdown("## 📊 Análisis extendido desde Correos")

    # Aplicaciones por empresa
    empresas_count = filtered_df["empresa_limpia"].value_counts().reset_index()
    empresas_count.columns = ["Empresa", "Aplicaciones"]
    fig_empresas_total = px.bar(
        empresas_count,
        x="Aplicaciones",
        y="Empresa",
        orientation="h",
        title="Aplicaciones por Empresa (Correos)",
        height=600
    )
    st.plotly_chart(fig_empresas_total, use_container_width=True)

    # Top 10 empresas
    top_empresas = empresas_count.head(10)
    fig_empresas = px.bar(top_empresas, x="Empresa", y="Aplicaciones", title="Top 10 Empresas (Correos)")
    st.plotly_chart(fig_empresas, use_container_width=True)



    # Top 10 puestos
    top_puestos = filtered_df["subject"].value_counts().nlargest(10).reset_index()
    top_puestos.columns = ["Puesto", "Aplicaciones"]
    fig_puestos = px.bar(top_puestos, x="Puesto", y="Aplicaciones", title="Top 10 Puestos (Correos)")
    st.plotly_chart(fig_puestos, use_container_width=True)


# ===========================
# TAB 2 - CSV Manual
# ===========================
with tab2:
    st.subheader("📂 Análisis de Aplicaciones desde CSV")

    try:
        df_apps = pd.read_csv("data/job_Applications.csv")
        df_apps.columns = df_apps.columns.str.strip().str.lower()
        df_apps.rename(columns={
            "application date": "fecha_aplicacion",
            "company name": "empresa",
            "job title": "puesto"
        }, inplace=True)

        df_apps["fecha_aplicacion"] = pd.to_datetime(
            df_apps["fecha_aplicacion"],
            format="%m/%d/%y, %I:%M %p",
            errors="coerce"
        )

        df_apps.dropna(subset=["fecha_aplicacion"], inplace=True)
    except Exception as e:
        st.error(f"No se pudo cargar el CSV de aplicaciones: {e}")
        st.stop()

    # Mostrar tabla
    st.markdown("### 🗂️ Aplicaciones registradas")
    st.dataframe(df_apps, use_container_width=True)

    # FILTRAR SOLO AÑO 2025
    df_apps = df_apps[df_apps["fecha_aplicacion"].dt.year == 2025]

    # Agrupar por mes y graficar línea
    df_apps["mes"] = df_apps["fecha_aplicacion"].dt.to_period("M").dt.to_timestamp()
    apps_por_mes_line = df_apps.groupby("mes").size().reset_index(name="Aplicaciones")

    fig_line = px.line(
        apps_por_mes_line,
        x="mes",
        y="Aplicaciones",
        markers=True,
        title="📈 Aplicaciones por Mes (solo 2025)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Aplicaciones por empresa
    empresas_count = df_apps["empresa"].value_counts().reset_index()
    empresas_count.columns = ["Empresa", "Aplicaciones"]
    fig_empresas_total = px.bar(
        empresas_count,
        x="Aplicaciones",
        y="Empresa",
        orientation="h",
        title="Aplicaciones por Empresa",
        height=600
    )
    st.plotly_chart(fig_empresas_total, use_container_width=True)

    # Top 10 empresas
    top_empresas = empresas_count.head(10)
    fig_empresas = px.bar(top_empresas, x="Empresa", y="Aplicaciones", title="Top 10 Empresas con más Aplicaciones")
    st.plotly_chart(fig_empresas, use_container_width=True)

    # Top 10 puestos
    top_titulos = df_apps["puesto"].value_counts().nlargest(10).reset_index()
    top_titulos.columns = ["Puesto", "Aplicaciones"]
    fig_titulos = px.bar(top_titulos, x="Puesto", y="Aplicaciones", title="Top 10 Puestos Aplicados")
    st.plotly_chart(fig_titulos, use_container_width=True)
