import unittest

from aziona.cli.parser.v1 import driver


class TestParserDriverV1(unittest.TestCase):
    def test_void_engine(self):
        try:
            engine = driver.ParserEgine({})
            self.assertEqual(engine.version, "1")
            self.assertEqual(engine.env, {})
            self.assertEqual(engine.targets, {})
            self.assertEqual(engine.options, driver.ParserOptionsStructure())
        except Exception:
            self.fail("Engine struttura errata")

    def test_void_engine_no_args(self):
        self.assertRaises(TypeError, driver.ParserEgine)


if __name__ == "__main__":
    unittest.main()
