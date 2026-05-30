from django.urls import path
from . import views

urlpatterns = [
    path(
        "weather/",
        views.weather_view
    ),
    path(
        "posts/",
        views.posts_view
    ),
    path(
    "api/weather-summary/",
    views.weather_summary_api
    )
    
]