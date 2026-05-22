import pandas as pd
import requests

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

all_data = []

for c in cities:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={c['lat']}&longitude={c['lon']}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_mean,relative_humidity_2m_mean"
        "&forecast_days=7"
        "&timezone=auto"
    )

    data = requests.get(url).json()

    df = pd.DataFrame({
        "City": c["city"],
        "Date": data["daily"]["time"],
        "High": data["daily"]["temperature_2m_max"],
        "Low": data["daily"]["temperature_2m_min"],
        "Humidity": data["daily"]["relative_humidity_2m_mean"],
        "Precipitation": data["daily"]["precipitation_probability_mean"]
    })

    all_data.append(df)

final = pd.concat(all_data, ignore_index=True)
final.to_csv("weather_data.csv", index=False)

print("Data updated successfully")
