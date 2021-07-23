import unittest

from jsonschema import exceptions

from aziona.cli.parser import parser
from aziona.core.conf import errors, settings


class TestParser(unittest.TestCase):
    def test_aziona_file_not_exist(self):
        file = "tests/cli/.abc.yml"

        self.assertRaises(errors.FileNotFoundError, parser.Parser, filename=file)

    def test_aziona_file_with_error(self):
        file = "tests/mock/.aziona-fail.yml"

        self.assertRaises(exceptions.ValidationError, parser.Parser, filename=file)

    def test_load_jsonschema_version(self):
        released = settings.getconst("PARSER").get("released")

        for v in released:
            try:
                parser.load_jsonschema(version=v)
            except Exception:
                self.fail("Schema %s not found" % v)

    def test_load_jsonschema_version_fail(self):
        self.assertRaises(
            errors.FileNotFoundError, parser.load_jsonschema, version="fail"
        )

    def test_aziona_file_with_success(self):
        file = "tests/mock/.aziona-valid.yml"
        try:
            parser.Parser(filename=file)
        except Exception:
            self.fail("Validazione spec fallita")


if __name__ == "__main__":
    unittest.main()
