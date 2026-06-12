from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import os
from .services.weather_service import get_weather_summary
from .services.jsonplaceholder_service import posts_per_user

from .services.weather_service import (
    get_weather,
    generate_chart,
)


def weather_view(request):
    latitude = request.GET.get("lat", 54.352)   # Gdańsk fallback
    longitude = request.GET.get("lon", 18.6466)

    weather = get_weather(latitude, longitude)

    
    if "error" in weather:
        return render(request, "external_data/weather.html", {
            "error": weather["error"],
            "status_code": weather.get("status_code"),
        })


    times = weather.get("times", [])
    temperatures = weather.get("temperatures", [])

    return render(request, "external_data/weather.html", {
        "times": times,
        "temperatures": temperatures,
        "current_temperature": weather.get("current_temperature"),
    })
def posts_view(request):

    stats = posts_per_user()

    return render(
        request,
        "external_data/posts.html",
        {
            "stats": stats.items()
        }
    )
def weather_summary_api(request):
    latitude = 54.3520
    longitude = 18.6466

    weather = get_weather_summary(latitude, longitude)

    temps = weather["temperatures"]

    avg_temp = (
        sum(temps)
        / len(temps)
    )

    return JsonResponse({
        "average_temperature":
            round(avg_temp, 2),

        "current_temperature":
            weather["current_temp"]
    })