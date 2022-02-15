import sys

from aziona.core import io
from aziona.services.parser import parser


def main(payload) -> bool:
    try:
        print(payload)
        parsed = parser.Parser(filename=payload["data"]["file"])
        parsed.main(payload["data"]["targets"])
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
