from . import python

__interpreter__ = {"python": python.Python}


def get(name: str):
    return __interpreter__.get(name)
