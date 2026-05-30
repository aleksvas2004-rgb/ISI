import requests
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import requests

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

        # sprawdzenie kodu HTTP
        if response.status_code != 200:
            return {
                "error": "API error",
                "status_code": response.status_code
            }

        data = response.json()

        times = [
            t.split("T")[1]
            for t in data["hourly"]["time"][:24]
        ]

        temperatures = data["hourly"]["temperature_2m"][:24]

        return {
            "times": times,
            "temperatures": temperatures,
            "current_temperature": temperatures[0]
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout"
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": "Connection error"
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": "Request failed",
            "details": str(e)
        }



def generate_chart(times, temperatures, filename):
    plt.figure(figsize=(10, 4))

    plt.plot(times, temperatures)

    plt.title("Temperatura - najbliższe 24h")
    plt.xlabel("Czas")
    plt.ylabel("°C")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()

def get_weather_summary(latitude, longitude):

    data = get_weather(latitude, longitude)

    times = data["times"][:24]
    temps = data["temperatures"][:24]

    return {
        "times": times,
        "temperatures": temps,
        "current_temp": temps[0]
    }