from resources.weather.weatherman import Weatherman
from rest_framework.views import APIView
from service.utils import ShortResponse, get_param_or_404


class Weather(APIView):
    def get(self, request):
        params = request.query_params
        city = get_param_or_404(params, "city")
        country = get_param_or_404(params, "country")
        try:
            result = Weatherman().get_current_weather(city, country)
            ShortResponse(200, result)
        except Exception as e:
            ShortResponse(500, str(e))
