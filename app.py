import streamlit as st
import requests
import pandas as pd

# ---------------------------
# 🌎 CIUDADES
# ---------------------------
cities = [
    {"city": "Ciudad Constitución, BCS, MX", "lat": 25.0325, "lon": -111.6643},
    {"city": "Trujillo, North Peru", "lat": -8.1116, "lon": -79.0287},
    {"city": "Ica, South Peru", "lat": -14.0678, "lon": -75.7286},
    {"city": "San Luis Río Colorado, SON, MX", "lat": 32.4519, "lon": -114.7714},
    {"city": "Caborca, SON, MX", "lat": 30.7086, "lon": -112.1580},
    {"city": "Sonoyta, SON, MX", "lat": 31.8616, "lon": -112.8493},
    {"city": "Mexicali, BCN, MX", "lat": 32.6245, "lon": -115.4523},
    {"city": "Ciudad Obregón, SON, MX", "lat": 27.4828, "lon": -109.9304},
    {"city": "Irapuato, GTO, MX", "lat": 20.6767, "lon": -101.3563}
]

# ---------------------------
# 🔧 FUNCIÓN API
# ---------------------------
def get_weather(city, lat, lon):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_mean,relative_humidity_2m_mean&timezone=auto"

    data = requests.get(url).json()

    df = pd.DataFrame({
        "City": city,
        "Date": data["daily"]["time"],
        "High": data["daily"]["temperature_2m_max"],
        "Low": data["daily"]["temperature_2m_min"],
        "Humidity": data["daily"]["relative_humidity_2m_mean"],
        "Precipitation": data["daily"]["precipitation_probability_mean"]
    })

    return df


# ---------------------------
# 📊 CONSTRUIR DATASET
# ---------------------------
all_data = []

for c in cities:
    df_city = get_weather(c["city"], c["lat"], c["lon"])
    all_data.append(df_city)

if all_data:
    df = pd.concat(all_data, ignore_index=True)
    df = df.sort_values(by=["City", "Date"])
else:
    df = pd.DataFrame(columns=["City", "Date", "High", "Low", "Humidity", "Precipitation"])


# ---------------------------
# 🌐 STREAMLIT UI
# ---------------------------
st.title("🌤 Weather Executive Dashboard")

st.subheader("Multi-City Forecast Report")

# 🔎 filtro por ciudad
city_filter = st.selectbox("Select City", ["All"] + list(df["City"].unique()))

if city_filter != "All":
    df = df[df["City"] == city_filter]

# 📊 métricas rápidas
col1, col2, col3 = st.columns(3)

col1.metric("Max Temp", df["High"].max())
col2.metric("Min Temp", df["Low"].min())
col3.metric("Cities", len(df["City"].unique()))

# 📋 tabla
st.dataframe(df)

# 📈 gráfico simple
st.line_chart(df[["High", "Low"]])
