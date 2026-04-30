import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📡 Dashboard IoT")

# Subir archivo
file = st.file_uploader("Sube tu archivo iot_data.csv", type=["csv"])

if file:
    df = pd.read_csv(file)

    # Convertir a datetime si existe columna de tiempo
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    st.subheader("📄 Datos")
    st.write(df.head())

    # ---------------------------
    # 🔎 FILTROS INTERACTIVOS
    # ---------------------------
    st.sidebar.header("Filtros")

    # Filtro por device_id
    if "device_id" in df.columns:
        devices = df["device_id"].unique()
        selected_device = st.sidebar.selectbox("Selecciona device_id", devices)
        df = df[df["device_id"] == selected_device]

    # Filtro por rango de fechas
    if "timestamp" in df.columns:
        min_date = df["timestamp"].min()
        max_date = df["timestamp"].max()

        date_range = st.sidebar.date_input(
            "Selecciona rango de fechas",
            [min_date, max_date]
        )

        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df["timestamp"] >= pd.to_datetime(start_date)) &
                    (df["timestamp"] <= pd.to_datetime(end_date))]

    # ---------------------------
    # 📊 ESTADÍSTICAS
    # ---------------------------
    st.subheader("📊 Estadísticas básicas")

    col1, col2, col3 = st.columns(3)

    col1.metric("🌡️ Temp promedio", round(df["temperature"].mean(), 2))
    col2.metric("⚡ Consumo promedio", round(df["energy_consumption"].mean(), 2))
    col3.metric("📳 Vibración máxima", round(df["vibration"].max(), 2))

    # Conteo de estados
    st.write("### Conteo de estados")
    if "status" in df.columns:
        status_counts = df["status"].value_counts()
        st.write(status_counts)

    # ---------------------------
    # 📈 VISUALIZACIONES
    # ---------------------------
    st.subheader("📈 Visualizaciones")

    # 📈 Serie de tiempo
    st.write("### Temperatura vs Tiempo")
    fig1, ax1 = plt.subplots()
    if "timestamp" in df.columns:
        ax1.plot(df["timestamp"], df["temperature"])
        ax1.set_xlabel("Tiempo")
    else:
        ax1.plot(df["temperature"])
    ax1.set_ylabel("Temperatura")
    st.pyplot(fig1)

    # 📊 Histograma
    st.write("### Histograma de consumo energético")
    fig2, ax2 = plt.subplots()
    ax2.hist(df["energy_consumption"], bins=20)
    ax2.set_xlabel("Consumo energético")
    st.pyplot(fig2)

    # 🔍 Relación entre variables
    st.write("### Temperatura vs Consumo energético")
    fig3, ax3 = plt.subplots()
    ax3.scatter(df["temperature"], df["energy_consumption"])
    ax3.set_xlabel("Temperatura")
    ax3.set_ylabel("Consumo energético")
    st.pyplot(fig3)

    # ---------------------------
    # 💡 INSIGHTS
    # ---------------------------
    st.subheader("💡 Insights")

    temp_prom = df["temperature"].mean()
    fail_count = 0

    if "status" in df.columns:
        fail_count = (df["status"] == "FAIL").sum()

    if temp_prom > 30:
        st.warning("⚠️ Temperatura promedio alta (>30°C)")

    if fail_count > 0:
        st.error(f"🚨 Hay {fail_count} registros en estado FAIL")

    if temp_prom <= 30 and fail_count == 0:
        st.success("✅ Sistema funcionando dentro de parámetros normales")
