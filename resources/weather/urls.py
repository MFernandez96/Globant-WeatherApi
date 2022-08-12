from django.urls import path
from resources.weather.views import Weather

urlpatterns = [
    path(
        "weather/",
        Weather.as_view(),
        name="get_weather_info",
    ),
]
