import importlib
import json
import os
import shlex

import jsonschema

from aziona.core import files, io
from aziona.core.conf import errors, settings


def get_schema_path(version: str):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "v%s" % version)


def load_jsonschema(version: str = None):
    if version is None or not isinstance(version, str):
        version = str(settings.getconst("PARSER").get("stable"))

    filename = os.path.join(get_schema_path(version), "schema.json")

    if not os.path.exists(filename):
        raise errors.FileNotFoundError(filename=filename)

    with open(filename) as fh:
        return json.load(fh)


def validate_aziona_schema(data: dict):
    schema = load_jsonschema(version=data.get("version"))

    jsonschema.validate(instance=data, schema=schema)


class Parser(object):
    raw: dict
    filename: str
    driver = None

    def __init__(self, filename: str):
        if not os.path.isfile(filename):
            raise errors.FileNotFoundError(filename=filename)

        self.filename = filename
        self.raw = self._get_raw()
        self.driver = self._get_driver()

    def _validation_schema(self):
        validate_aziona_schema(data=self.raw)

    def _get_raw(self):
        if not isinstance(self.filename, str):
            raise errors.ExcptionError(message="self.filename non valido")
        return files.yaml_load(self.filename)

    def _get_driver(self):
        self._validation_schema()

        try:
            if self.raw.get("version") is None:
                raise errors.ExcptionError(message="Versione parser non trovata")

            _module = importlib.import_module(
                "aziona.cli.parser.v%s.driver" % self.raw.get("version")
            )
            return _module.ParserEgine(self.raw)
        except Exception as e:
            raise io.exception(e)

    def main(self, targets):
        if not self.driver:
            raise errors.ExcptionError(message="Driver non inizializzato")

        if isinstance(self.driver, str):
            targets = shlex.split(targets)

        if not isinstance(targets, list):
            raise errors.ParamTypeError(param="driver", type="list")

        self.driver.main(*targets)
