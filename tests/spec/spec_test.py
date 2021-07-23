import json
import unittest

from jsonschema import exceptions, validate

from aziona.cli.parser import parser
from aziona.core.conf import settings
from aziona.core.files import yaml_load

SCHEMA = parser.load_jsonschema(version=settings.getconst("PARSER").get("stable"))


class TestAzionaSpec(unittest.TestCase):
    def test_fail_json(self):
        data = json.load(open("tests/mock/.aziona-fail.json", "r"))

        self.assertRaises(
            exceptions.ValidationError, validate, instance=data, schema=SCHEMA
        )

    def test_valid_json(self):
        data = json.load(open("tests/mock/.aziona-valid.json", "r"))
        try:
            validate(instance=data, schema=SCHEMA)
        except Exception:
            self.fail("Validazione spec fallita")

    def test_fail_yaml(self):
        data = yaml_load("tests/mock/.aziona-fail.yml")
        self.assertRaises(
            exceptions.ValidationError, validate, instance=data, schema=SCHEMA
        )

    def test_valid_yaml(self):
        data = yaml_load("tests/mock/.aziona-valid.yml")
        try:
            validate(instance=data, schema=SCHEMA)
        except Exception:
            self.fail("Validazione spec fallita")


if __name__ == "__main__":
    unittest.main()
