# -*- coding: utf-8 -*-
"""Il modulo text.py funzioni per la manipolazione del testo e interpolazione delle variabile al suo interno
"""
import dataclasses
import json
import re
import sys
import tempfile

from aziona.core import commands, io
from aziona.core.conf import errors, settings

re_newlines = re.compile(r"\r\n|\r")  # Used in normalize_newlines
re_camel_case = re.compile(r"(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))")


def normalize_newlines(text):
    return re_newlines.sub("\n", str(text))


def camel_case_to_spaces(value):
    """
    Split CamelCase and convert to lowercase. Strip surrounding whitespace.
    """
    return re_camel_case.sub(r" \1", value).strip().lower()


class DataclassesJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def interpolation_bash(value: str, env: dict = {}) -> str:
    if value is None:
        return ""

    if not isinstance(value, str):
        raise errors.ExcptionError(message="param 'value' is not str")

    env = {**settings.environ(), **env}

    matchs = re.findall(r"(?<=\$\()(.*?)(?=\))", value)

    for item in matchs:
        stdout = commands.exec_output(item, env=env)
        value = value.replace("$(%s)" % item, stdout)

    return value


def interpolation_vars(values, from_dict={}):
    """Consente di interpolare dei valori all'inerno di una stringa.

    Verranno interpolate esclusivamente i valori all'interno della stringa che sono tra ${...}, il valore \
    che andrà a sostituire
    la variabile sarà preso dal dizionario passato (param from_dict) oppure dall'environ. \
    La stringa potrà contere più varibili da interpolare (anche con differenti nomi),

    Examples:
        Nell'environ deve esserci la varibile TEST=xyz e PATH=/, \
        oppure passare il parametro from_dict con il valore {'TEST':'xyz', 'PATH':'/'}

        values = "test ${TEST}" =>  "test xyz"
        values = ['test','${TEST}'] => ['test', 'xyz']
        values = {'a':'test','b':'${TEST}'} => {'a':'test','b':'xyz'}
        values = "${PATH}${TEST}" =>  "/xyz"
        values = ['test','${PATH}${TEST}'] => ['test', '/xyz']
        values = {'a':'test','b':'${PATH}${TEST}'} => {'a':'test','b':''}

    Args:
        values(str,dict,list): valori che vengolo elaborati sostituendo le str \
            (o i valori delle chiavi per quanto riguarda i dict) solo se inziano con il simbolo $
        from_dict (dict): dizionario da cui andare a prendere i valori da interpolare, se vuoto utilizza os.environ

    Returns:
        str,dict,list: a secondo del tipo del parametro values

    Raises:
        Exception generiche
    """

    def _dataset(key, **kwargs: str):
        if kwargs.get(key):
            return kwargs.get(key)

        if from_dict.get(key):
            return from_dict.get(key)

        return settings.environ().get(key, "")

    def _make_interpolation_str(key, **kwargs: str):
        if key is None:
            return ""

        if isinstance(key, (bool, int, float)):
            return key

        if isinstance(key, list):
            res = []
            for value in key:
                res.append(_make_interpolation_str(value, **kwargs))
            return res

        if isinstance(key, dict):
            res = {}
            for value_key, value_item in key.items():
                res[value_key] = _make_interpolation_str(value_item, **kwargs)
            return res

        if isinstance(key, str):
            matchs = re.findall(r"(?<=\${)(.*?)(?=})", key)
            key = interpolation_bash(key, from_dict)
            for item in matchs:
                key = key.replace("${%s}" % item, _dataset(item, **kwargs))
            return key

    def _str(data):
        return _make_interpolation_str(data)

    def _dict(data):
        res = {}
        for (key, value) in data.items():
            res[key] = _make_interpolation_str(value, **res)
        return res

    def _list(data):
        res = []
        for item in data:
            res.append(_make_interpolation_str(item))
        return res

    if isinstance(values, str):
        return _str(values)

    if isinstance(values, dict):
        return _dict(values)

    if isinstance(values, list):
        return _list(values)

    return values


def interpolation_file(
    filename: str, from_dict: dict = {}, overwrite: bool = False
) -> str:
    with open(filename, "r+") as f:
        output = interpolation_vars(f.read(), from_dict)
        if overwrite is True:
            f.seek(0)
            f.write(output)
    return output


def jq(data: str, query, xargs: bool = False) -> str:
    if not isinstance(data, str):
        raise errors.ParamTypeError(param="data", type="str")

    if isinstance(query, (dict, list)):
        query = " ".join(query)

    if not isinstance(query, str):
        raise errors.ParamTypeError(param="query", type="str")

    temp = tempfile.NamedTemporaryFile(mode="w")

    try:
        temp.write(data)
        temp.seek(0)
        cmd = "cat %s | jq -r '%s' %s" % (
            temp.name,
            query,
            (" | xargs" if xargs is True else ""),
        )
        io.debug(cmd)
        return commands.exec_output(cmd)
    finally:
        temp.close()


def str_to_sysencoding(bytestring):
    """Converte byte stringhe

    Args:
        bytestring(str): stringa con caratteri speciali

    Returns:
        str:

    Raises:
        None
    """
    bytestring = str(bytestring).encode()
    return bytestring.decode(sys.getfilesystemencoding())
