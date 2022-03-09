# -*- coding: utf-8 -*-
"""Il modulo files.py espone le funzionalità per gesitre azioni specifiche nel filesystem.
"""
import json
import os

import yaml

from aziona import errors


def isfile(filename: str, with_raise: bool = False):
    if not os.path.isfile(filename):
        if with_raise:
            raise errors.FileNotFoundError(filename=filename)
        return False
    return True


def abspath(*args, os_path=True, separator='/'):
    path = separator.join(args)
    if os_path is True:
        from pathlib import Path

        return str(Path(path))
    return path


def json_load(filename: str):
    filename = abspath(filename)

    if not os.path.exists(filename):
        raise errors.FileNotFoundError(filename=filename)

    with open(filename) as fh:
        return json.load(fh)


def yaml_dump(filename, data, **opt):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, **opt)


def yaml_load(filename, loader=yaml.SafeLoader):
    if not os.path.isfile(filename):
        raise OSError('Is not file: %s' % filename)

    with open(filename, 'r') as fileobj:
        return yaml.load(fileobj, Loader=loader)
