import inspect


class Injector:
    def __init__(self):
        self._services = {}

    def bind(self, base: type, instance: any):
        if not isinstance(instance, base):
            raise TypeError(f'Instance must be instance of {base}')

        self._services.update({base: instance})

    def inject(self, func):
        def wrapper(*args, **kwargs):
            signature = inspect.signature(func)
            for param_name, param in signature.parameters.items():
                if not param.default:
                    base = param.annotation
                    if base in self._services:
                        kwargs.update({param_name: self._services[base]})
            result = func(*args, **kwargs)
            return result

        return wrapper

    def get_dependency(self, base: type):
        if base in self._services:
            return self._services[base]
        raise ValueError(f'Service not found: {base}')
