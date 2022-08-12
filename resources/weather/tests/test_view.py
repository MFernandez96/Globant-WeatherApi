import json
from collections import namedtuple

import pytest
from resources.weather.views import Weather

pytestmark = pytest.mark.django_db


def test_weather_view():
    request = namedtuple("Request", ["query_params"])
    request.query_params = {"city": "London", "country": "UK"}
    response = Weather().get(request)
    data = json.loads(response.content)
    assert response.__getitem__("Content-Type") == "application/json"
    assert set(data.keys()) == {
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
    assert type(data["forecast"]) == dict
    first_forecast = next(iter(data["forecast"]))
    assert set(data["forecast"][first_forecast].keys()) == {
        "pressure",
        "temperature",
        "humidity",
        "wind",
        "sunrise",
        "sunset",
        "cloudiness",
        "geo_coordinates",
    }


def test_failing_weather_view():
    request = namedtuple("Request", ["query_params"])
    request.query_params = {"city": "London", "country": None}
    with pytest.raises(Exception):
        response = Weather().get(request)
