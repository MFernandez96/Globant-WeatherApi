from collections import namedtuple

import pytest
from resources.weather.weatherman import Weatherman
import json

pytestmark = pytest.mark.django_db


def test_weather_api():
    api = Weatherman("London", "UK").setup_api_data()
    assert api.weather.keys() == {
        "base",
        "clouds",
        "cod",
        "coord",
        "dt",
        "id",
        "main",
        "name",
        "sys",
        "timezone",
        "visibility",
        "weather",
        "wind",
    }
    assert api.forecast.keys() == {"city", "cnt", "cod", "list", "message"}

    request = namedtuple("Request", ["query_params"])
    request.query_params = {"city": "London", "country": "UK"}
    response = Weather().get(request)
    data = json.loads(response.content)
    assert response.__getitem__("Content-Type") == "application/json"
    assert data.keys() == {
        "location_name",
        "temperature",
        "wind",
        "cloudiness",
        "pressure",
        "humidity",
        "sunrise",
        "sunset",
        "geo_coordinates",
        "requested_time",
        "forecast",
    }
