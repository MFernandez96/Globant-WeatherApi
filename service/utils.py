from django.http import JsonResponse

from service.middleware import ParamNotFound


def ShortResponse(status: int = 200, message: str = None, safe: bool = True, **kwargs):
    data = {"status": status, "msg": message}
    data.update(kwargs)
    return JsonResponse(data, status=status, safe=safe)


def get_param_or_404(params, param_name: str):
    param = params.get(param_name, None)
    if param is None:
        raise ParamNotFound(f"Parameter {param_name} not found")
    return param
