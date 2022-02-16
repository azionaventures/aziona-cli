import os

import jsonschema
from packaging import version

from aziona.services.translator.parser import v1
from aziona.services.utilities import files

SCHEMA_VERSION = {
    v1.parser.VERSION: {
        "parser": v1.parser.ParserEngine,
        "schema": files.abspath(
            os.path.dirname(os.path.abspath(__file__)), "parser", "v1", "schema.json"
        ),
    }
}

SCHEMA_DEFAULT_VERSION = v1.parser.VERSION


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

        _parser, self.schema = self.validate()

        self.parser = _parser(self.raw)

    def validate(self):
        schema_version = SCHEMA_VERSION.get(self.version)

        schema = files.json_load(schema_version["schema"])

        jsonschema.validate(instance=self.raw, schema=schema)

        return schema_version["parser"], schema_version["schema"]
