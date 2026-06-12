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

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {
                "error": "API error",
                "status_code": response.status_code
            }

        data = response.json()

        hourly = data.get("hourly", {})
        times_raw = hourly.get("time", [])
        temps_raw = hourly.get("temperature_2m", [])

        if not times_raw or not temps_raw:
            return {"error": "Missing hourly data from API"}

        times = [t.split("T")[1] for t in times_raw[:24]]
        temperatures = temps_raw[:24]

        return {
            "times": times,
            "temperatures": temperatures,
            "current_temperature": temperatures[0] if temperatures else None
        }

    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}

    except requests.exceptions.ConnectionError:
        return {"error": "Connection error"}

    except requests.exceptions.RequestException as e:
        return {
            "error": "Request failed",
            "details": str(e)
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