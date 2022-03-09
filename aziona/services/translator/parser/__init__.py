from aziona import errors


class MapStructure(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(MapStructure, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(MapStructure, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(MapStructure, self).__delitem__(key)
        del self.__dict__[key]


class BaseParserEgine(object):
    _schema_info = {'deprecated': {}, 'warning': {}, 'errors': {}}
    _raw: dict = None

    def __init__(self, raw: dict) -> None:
        if not isinstance(raw, dict):
            raise errors.ParamTypeError(param='raw', type='dict')

        self._raw = MapStructure(raw)

        self.run()

    def run(self) -> str:
        raise errors.MethodNotImplemented(method='run')

    def __str__(self) -> str:
        return str({k: v for k, v in self.__dict__.items() if not k.startswith('_')})
