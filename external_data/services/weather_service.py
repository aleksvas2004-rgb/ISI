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

    response = requests.get(url)
    response.raise_for_status()

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