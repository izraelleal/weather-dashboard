import streamlit as st
import pandas as pd

st.title("🌤 Weather Executive Dashboard (PRO)")

# 📊 cargar snapshot (NO API)
df = pd.read_csv("weather_data.csv")

df = df.sort_values(by=["City", "Date"])

# 🔎 filtro
city = st.selectbox("Select City", ["All"] + list(df["City"].unique()))

if city != "All":
    df = df[df["City"] == city]

# 📊 KPIs
col1, col2, col3 = st.columns(3)

col1.metric("🌡 Max Temp", f"{df['High'].max()}°C")
col2.metric("❄ Min Temp", f"{df['Low'].min()}°C")
col3.metric("🌎 Cities", df["City"].nunique())

# 📋 tabla
st.dataframe(df, use_container_width=True)

# 📈 chart
st.line_chart(df.set_index("Date")[["High", "Low"]])
