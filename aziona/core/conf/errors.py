class BaseAzionaError(Exception):
    message_format = "Errore non specificato"

    def __init__(self, status: int = None, **kwargs):
        message = self.message_format.format(**kwargs)
        self.errors = {
            "exception": self.__class__.__name__,
            "message": message,
            "status": status,
            "kwargs": kwargs,
        }
        Exception.__init__(self, message)


class ExcptionError(BaseAzionaError):
    message_format = "{message}"


class ParamTypeError(BaseAzionaError):
    message_format = "Param '{param}' is not '{type}'"


class CriticalError(BaseAzionaError):
    message_format = "Errore critico: {message}"


class FileNotFoundError(BaseAzionaError):
    message_format = "File {filename} not found"


class ExcpetionNotValidError(BaseAzionaError):
    message_format = "Exception errata: {exception}"
