import os
from datetime import datetime

import requests
from django.core.cache import cache


class Weatherman(object):
    def __init__(self, city: str, country: str) -> None:
        self.city = city
        self.country = country

    def get_current_weather(self) -> dict:
        self.setup_api_data()
        return self.get_current_weather_data()

    def setup_api_data(self):
        self.retrieve_from_cache()
        if not self.weather or not self.forecast:
            self.get_from_api()

    def get_from_api(self):
        self.weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&appid={os.getenv("OPENWEATHER_API_KEY")}'
        self.forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={self.city},{self.country}&appid={os.getenv("OPENWEATHER_API_KEY")}'
        self.weather = requests.get(self.weather_url).json()
        self.forecast = requests.get(self.forecast_url).json()
        cache.set("weather", self.weather, timeout=120)
        cache.set("forecast", self.forecast, timeout=120)

    def retrieve_from_cache(self):
        self.weather = cache.get("weather")
        self.forecast = cache.get("forecast")

    def get_temperature_in_celsius(self, temperature):
        temperature_in_celsius = int(temperature) - 273.15
        return round(temperature_in_celsius, 2)

    def get_temperature_in_fahrenheit(self, temperature):
        temperature_in_fahrenheit = int(temperature) * 9 / 5 - 459.67
        return round(temperature_in_fahrenheit, 2)

    def degrees_to_compass(self, degrees):
        deg = int((degrees / 22.5) + 0.5)
        compass = [
            "north",
            "north-north-east",
            "north-east",
            "east-north-east",
            "east",
            "east-south-east",
            "south-east",
            "south-south-east",
            "south",
            "south-south-west",
            "south-west",
            "west-south-west",
            "west",
            "west-north-west",
            "north-west",
            "north-north-west",
        ]
        return compass[(deg % 16)]

    def utc_time_convertion(self, time):
        utc_time = datetime.fromtimestamp(time)
        return utc_time.strftime("%H:%M")

    def get_forecast_weather_data(self):
        forecast_list = self.forecast["list"]
        return [
            {
                "temperature": f"{self.get_temperature_in_celsius(weather['main']['temp'])} °C, {self.get_temperature_in_fahrenheit(weather['main']['temp'])} °F",
                "wind": f"{beaufort_scale.beaufort_scale_ms(self.weather['wind']['speed'], language='en')}, {self.weather['wind']['speed']} m/s, {self.degrees_to_compass(self.weather['wind']['deg'])}",
                "cloudiness": weather["weather"][0]["description"],
                "humidity": f"{weather['main']['humidity']}%",
                "time": weather["dt_txt"],
            }
            for weather in forecast_list
        ]

    def get_current_weather_data(self):
        return {
            "location_name": f"{self.weather['name']}, {self.weather['sys']['country']}",
            "temperature": f"{self.get_temperature_in_celsius(self.weather['main']['temp'])} °C, {self.get_temperature_in_fahrenheit(self.weather['main']['temp'])} °F",
            "wind": f"{beaufort_scale.beaufort_scale_ms(self.weather['wind']['speed'], language='en')}, {self.weather['wind']['speed']} m/s, {self.degrees_to_compass(self.weather['wind']['deg'])}",
            "cloudiness": self.weather["weather"][0]["description"],
            "pressure": f"{self.weather['main']['pressure']} hPa",
            "humidity": f"{self.weather['main']['humidity']}%",
            "sunrise": f"{self.utc_time_convertion(self.weather['sys']['sunrise'])}",
            "sunset": f"{self.utc_time_convertion(self.weather['sys']['sunset'])}",
            "geo_coordinates": f"[{self.weather['coord']['lat']}, {self.weather['coord']['lon']}]",
            "requested_time": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "forecast": self.get_forecast_weather_data(),
        }
