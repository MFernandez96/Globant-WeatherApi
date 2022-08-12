from service.middleware import ParamNotFound


def get_param_or_404(params, param_name: str):
    param = params.get(param_name, None)
    if param is None:
        raise ParamNotFound(f"Parameter {param_name} not found")
    return param
