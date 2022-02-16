from aziona.core.conf import errors


class BaseParserEgine(object):
    schema_info = {"deprecated": {}, "warning": {}, "errors": {}}
    raw: dict = None

    def __init__(self, raw: dict) -> None:
        if not isinstance(raw, dict):
            raise errors.ParamTypeError(param="raw", type="dict")

    def __str__(self) -> str:
        return str(self.__dict__)
