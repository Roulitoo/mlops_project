import requests
import json
from datetime import datetime, UTC

url = "https://api.open-meteo.com/v1/forecast"
params = {
        "latitude": 48.8566,
        "longitude": 2.3522,  # Paris coordinates
    "hourly": ",".join([
        "temperature_2m",
        "precipitation",
        "relative_humidity_2m",
        "dew_point_2m",
        "apparent_temperature",
        "cloudcover",
        "windspeed_10m",
        "winddirection_10m",
        "shortwave_radiation",
        "surface_pressure"
    ])
}
resp = requests.get(url, params=params)
data = resp.json()

filename = f"data/raw/{datetime.now(UTC):%Y-%m-%d}.json"
with open(filename, "w") as f:
    json.dump(data, f)