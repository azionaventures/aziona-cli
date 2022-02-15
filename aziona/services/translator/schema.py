import os
import shlex

import jsonschema
from packaging import version

from aziona.core.conf import errors
from aziona.services.translator import v1
from aziona.services.utilities import files

SCHEMA_VERSION = {
    version.parse("1.0"): {
        "parser": v1.parser,
        "schema": files.abspath(
            os.path.dirname(os.path.abspath(__file__)), "v1", "schema.json"
        ),
    }
}

SCHEMA_DEFAULT_VERSION = version.parse("1.0")


class Schema(object):
    version: int
    raw: dict
    filename: str
    parser = None

    def __init__(self, filename: str):
        files.isfile(filename, with_raise=True)

        self.filename = filename

        self.raw = files.yaml_load(self.filename)

        self.version = (
            version.parse(self.raw.get("version"))
            if self.raw.get("version")
            else SCHEMA_DEFAULT_VERSION
        )

        self.parser, self.schema = self.validate()

        self.parser = self.parser.ParserEgine(self.raw)

    def validate(self):
        schema_version = SCHEMA_VERSION.get(self.version)

        schema = files.json_load(schema_version["schema"])

        jsonschema.validate(instance=self.raw, schema=schema)

        return schema_version["parser"], schema_version["schema"]

    def main(self, targets):
        if not self.parser:
            raise errors.ExcptionError(message="Driver non inizializzato")

        if isinstance(self.parser, str):
            targets = shlex.split(targets)

        if not isinstance(targets, list):
            raise errors.ParamTypeError(param="driver", type="list")

        self.parser.main(*targets)
