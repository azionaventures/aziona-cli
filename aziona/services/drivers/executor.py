import sys

from aziona.services.translator import translator
from aziona.services.utilities import io


def main(filename: str, targets: list) -> bool:
    try:
        schema = translator.Schema(filename=filename)
        print(schema.parser)
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
