import os
from datetime import datetime

import requests
from beaufort_scale import beaufort_scale_ms
from django.core.cache import cache


class Weatherman(object):
    def __init__(self, city: str, country: str) -> None:
        self.wind_utils = WindUtils()
        self.temp_utils = TempUtils()
        self.city = city
        self.country = country
        self.result = {}

    def get_current_weather(self) -> dict:
        self.setup_api_data()
        self.parse_weather_data()
        self.parse_forecast_data()
        return self.result

    def setup_api_data(self):
        self.retrieve_from_cache()
        if not self.weather or not self.forecast:
            self.get_from_api()

    def retrieve_from_cache(self):
        self.weather = cache.get("weather")
        self.forecast = cache.get("forecast")

    def get_from_api(self):
        self.weather_url = f"""http://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&appid={os.getenv("OPENWEATHER_API_KEY")}"""
        self.forecast_url = f"""http://api.openweathermap.org/data/2.5/forecast?q={self.city},{self.country}&appid={os.getenv("OPENWEATHER_API_KEY")}"""
        self.weather = requests.get(self.weather_url).json()
        self.forecast = requests.get(self.forecast_url).json()
        cache.set("weather", self.weather, timeout=120)
        cache.set("forecast", self.forecast, timeout=120)

    def parse_weather_data(self):
        self.result["location_name"] = f"""{self.city}, {self.country.upper()}"""
        self.result[
            "temperature"
        ] = f"""{self.temp_utils.kelvin_to_celsius(self.weather["main"]["temp"])} °C | {self.temp_utils.kelvin_to_fahrenheit(self.weather["main"]["temp"])} °F"""
        self.result[
            "wind"
        ] = f"""{beaufort_scale_ms(self.weather["wind"]["speed"])}, {self.weather["wind"]["speed"]} m/s, {self.wind_utils.degrees_to_compass(self.weather["wind"]["deg"])}"""
        self.result["cloudiness"] = self.weather["weather"][0]["description"]
        self.result["pressure"] = f"""{self.weather["main"]["pressure"]} hPa"""
        self.result["humidity"] = f"""{self.weather["main"]["humidity"]}%"""
        self.result["sunrise"] = datetime.utcfromtimestamp(
            self.weather["sys"]["sunrise"]
        ).strftime("%H:%M")
        self.result["sunset"] = datetime.utcfromtimestamp(
            self.weather["sys"]["sunset"]
        ).strftime("%H:%M")
        self.result[
            "geo_coordinates"
        ] = f"""{self.weather["coord"]["lon"]}, {self.weather["coord"]["lat"]}"""
        self.result["requested_time"] = datetime.utcfromtimestamp(
            self.weather["dt"]
        ).strftime("%Y-%m-%d %H:%M:%S")

    def parse_forecast_data(self):
        self.result["forecast"] = {}
        if self.forecast["cod"] == "200":
            forecast_data = {}
            for forecast in self.forecast["list"]:
                forecast_time = forecast["dt_txt"]
                forecast_data[forecast_time] = {
                    "temperature": f"""{int(self.temp_utils.kelvin_to_celsius(forecast["main"]["temp"]))} °C | {int(self.temp_utils.kelvin_to_fahrenheit(forecast["main"]["temp"]))} °F"""
                }

                forecast_data[forecast_time][
                    "wind"
                ] = f"""{beaufort_scale_ms(forecast["wind"]["speed"])}, {forecast["wind"]["speed"]} m/s, {self.wind_utils.degrees_to_compass(forecast["wind"]["deg"])}"""

                forecast_data[forecast_time]["cloudiness"] = forecast["weather"][0][
                    "description"
                ]

                forecast_data[forecast_time][
                    "humidity"
                ] = f"""{forecast["main"]["humidity"]}%"""

                forecast_data[forecast_time]["sunrise"] = datetime.utcfromtimestamp(
                    self.forecast["city"]["sunrise"]
                ).strftime("%H:%M")

                forecast_data[forecast_time]["sunset"] = datetime.utcfromtimestamp(
                    self.forecast["city"]["sunset"]
                ).strftime("%H:%M")

                forecast_data[forecast_time][
                    "geo_coordinates"
                ] = f"""{self.forecast["city"]["coord"]["lon"]}, {self.forecast["city"]["coord"]["lat"]}"""
            self.result["forecast"] = forecast_data
        else:
            self.result["forecast"] = {"msg": "No forecast available"}


class WindUtils:
    def degrees_to_compass(self, degrees: int) -> str:
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


class TempUtils:
    def kelvin_to_celsius(self, kelvin: float) -> float:
        return kelvin - 273.15

    def kelvin_to_fahrenheit(self, kelvin: float) -> float:
        return kelvin * 1.8 - 459.67
