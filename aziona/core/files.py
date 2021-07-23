# -*- coding: utf-8 -*-
"""Il modulo files.py espone le funzionalità per gesitre azioni specifiche nel filesystem.
"""
import os

import yaml


def yaml_dump(filename, data, **opt):
    with open(filename, "w") as outfile:
        yaml.dump(data, outfile, **opt)


def yaml_load(filename, loader=yaml.SafeLoader):
    """Parsa il file yaml indicato

    Args:
        filename(str): path del file yaml
        loader(yaml.Loader): loader yaml usato per il parsing del file

    Returns:
        str: path generato

    Raises:
    """
    if not os.path.isfile(filename):
        raise OSError("Is not file: %s" % filename)

    with open(filename, "r") as fileobj:
        return yaml.load(fileobj, Loader=loader)


def generate_path(*args, os_path=True, separator="/"):
    """Generatore di path utilizzando gli argomenti passati

    Args:
        os_path(bool): default True, consente di attivare o disattivare la convenzione del os
        separator(str,optional): default "/", consente di cambiare il separatore tra gli elementi args
        *args(str): valori che vengono uniti in modo sequenziale per generare il path

    Returns:
        str: path generato

    Raises:
        None
    """
    path = separator.join(args)
    if os_path is True:
        from pathlib import Path

        return str(Path(path))
    return path
