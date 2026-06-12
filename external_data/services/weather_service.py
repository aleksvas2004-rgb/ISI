import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_weather(latitude, longitude):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&hourly=temperature_2m"
        "&forecast_days=1"
    )

    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return {"error": "API error", "status_code": response.status_code}

    data = response.json()

    hourly = data.get("hourly", {})

    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])

    return {
        "times": [t.split("T")[1] for t in times[:24]],
        "temperatures": temps[:24],
        "current_temperature": temps[0] if temps else None
    }
def get_weather_summary(latitude, longitude):
    data = get_weather(latitude, longitude)

    if "error" in data:
        return data

    times = data.get("times", [])
    temps = data.get("temperatures", [])

    if not times or not temps:
        return {"error": "Empty weather data"}

    return {
        "times": times,
        "temperatures": temps,
        "current_temp": temps[0]
    }

def generate_chart(times, temperatures, filename):
    if not times or not temperatures:
        return {"error": "No data for chart"}

    plt.figure(figsize=(10, 4))
    plt.plot(times, temperatures)

    plt.title("Temperatura - najbliższe 24h")
    plt.xlabel("Czas")
    plt.ylabel("°C")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()