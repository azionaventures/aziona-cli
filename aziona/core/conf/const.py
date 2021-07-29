import sys
from distutils.version import LooseVersion

from aziona import __version__

NAME = "aziona"

VERSION = __version__

PARSER = {"stable": LooseVersion("1"), "released": ["1"]}

PARSER_INTERPRETER = {
    "default": "python3",
    "supported": {
        "python": "python -m {module} {args}",
        "python3": "python3 -m {module} {args}",
        "python2": "python2 -m {module} {args}",
        "python-func": "python -c '{module} {args}'",
        "python3-func": "python3 -c '{module} {args}'",
        "python2-func": "python2 -c '{module} {args}'",
        "bash": "/bin/bash -c '{module} {args}'",
        "sh": "/bin/sh -c '{module} {args}'",
    },
}

DEFAULT_CHARSET = "utf-8"

IS_WINDOWS_PLATFORM = sys.platform == "win32"

IS_LINUX_PLATFORM = sys.platform == "linux"

DEPENDETIES_REQUIRED = {
    "terraform": LooseVersion("0.13.3"),
    "docker": LooseVersion("20.10"),
    "kubernetes": LooseVersion("1.20"),
}

VERBOSITY_LEVEL = (LooseVersion("1"), LooseVersion("2"), LooseVersion("3"))


def getconst(key: str = None, default=None):
    return globals().get(key, default)


def get_interpreter(name: str):
    if name not in getconst("PARSER_INTERPRETER")["supported"].keys():
        raise Exception("Errore '%s' interprete non trovato" % name)

    return getconst("PARSER_INTERPRETER")["supported"][name]
