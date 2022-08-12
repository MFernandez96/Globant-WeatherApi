from collections import namedtuple

import pytest
from resources.weather.weatherman import WindUtils, TempUtils
import json

pytestmark = pytest.mark.django_db


@pytest.mark.skip(
    reason="TODO: find a good source, converter or calculator about wind direction"
)
def test_windutils():
    pass


def test_temputils():
    assert int(TempUtils().kelvin_to_celsius(500)) == 226
    assert int(TempUtils().kelvin_to_fahrenheit(40)) == -387
