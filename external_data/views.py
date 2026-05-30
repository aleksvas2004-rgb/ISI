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

    latitude = 54.3520
    longitude = 18.6466

    weather = get_weather(
        latitude,
        longitude
    )

    chart_path = os.path.join(
        settings.BASE_DIR,
        "media",
        "weather_chart.png"
    )

    generate_chart(
        weather["times"],
        weather["temperatures"],
        chart_path
    )

    return render(
        request,
        "external_data/weather.html",
        {
            "current_temp":
                weather["current_temperature"],
            "chart":
                "/media/weather_chart.png"
        }
    )
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