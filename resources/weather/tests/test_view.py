from collections import namedtuple

import pytest
from resources.weather.views import Weather
import json

pytestmark = pytest.mark.django_db


def test_weather_view():
    import ipdb

    ipdb.set_trace()
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
