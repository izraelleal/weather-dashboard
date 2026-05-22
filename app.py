import streamlit as st
import requests
import pandas as pd

# =========================
# 🌎 CIUDADES
# =========================
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

# =========================
# 🔧 API (CACHE POR CIUDAD)
# =========================
@st.cache_data(ttl=3600)
def get_weather(city, lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_mean,relative_humidity_2m_mean"
        "&forecast_days=7"
        "&timezone=auto"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    if "daily" not in data:
        return pd.DataFrame()

    return pd.DataFrame({
        "City": city,
        "Date": data["daily"]["time"],
        "High": data["daily"]["temperature_2m_max"],
        "Low": data["daily"]["temperature_2m_min"],
        "Humidity": data["daily"]["relative_humidity_2m_mean"],
        "Precipitation": data["daily"]["precipitation_probability_mean"]
    })


# =========================
# 📊 CACHE GLOBAL (CLAVE)
# =========================
@st.cache_data(ttl=3600)
def load_all_data():

    all_data = []

    for c in cities:
        df_city = get_weather(c["city"], c["lat"], c["lon"])
        if not df_city.empty:
            all_data.append(df_city)

    if len(all_data) == 0:
        return pd.DataFrame()

    return pd.concat(all_data, ignore_index=True)


# =========================
# 📊 LOAD DATA
# =========================
df = load_all_data()

if df.empty:
    st.error("No data available (API or cache issue)")
    st.stop()

df = df.sort_values(by=["City", "Date"])


# =========================
# 🌐 DASHBOARD UI
# =========================
st.title("🌤 Weather Executive Dashboard")
st.subheader("Multi-City Forecast System")

# 🔎 FILTRO
city_filter = st.selectbox("Select City", ["All"] + list(df["City"].unique()))

filtered_df = df.copy()

if city_filter != "All":
    filtered_df = filtered_df[filtered_df["City"] == city_filter]


# =========================
# 📊 KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("🌡 Max Temp", f"{filtered_df['High'].max()}°C")
col2.metric("❄ Min Temp", f"{filtered_df['Low'].min()}°C")
col3.metric("🌎 Cities", filtered_df["City"].nunique())


# =========================
# 📋 TABLE
# =========================
st.dataframe(filtered_df, use_container_width=True)


# =========================
# 📈 CHART
# =========================
st.line_chart(filtered_df.set_index("Date")[["High", "Low"]])
