from resources.weather.weatherman import Weatherman
from rest_framework.views import APIView
from service.utils import get_param_or_404
from django.http import JsonResponse


class Weather(APIView):
    def get(self, request):
        params = request.query_params
        city = get_param_or_404(params, "city")
        country = get_param_or_404(params, "country")
        try:
            result = Weatherman(city, country).get_current_weather()
            return JsonResponse(status=200, data=result)
        except Exception as e:
            return JsonResponse(status=500, data=str(e))
