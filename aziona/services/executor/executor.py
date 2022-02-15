import sys

from aziona.services.translator import schema
from aziona.services.utilities import io


def main(payload) -> bool:
    try:
        print(payload)

        # parsere il file aziona in base alla versione e ritornare

        parsed = schema.Schema(filename=payload["data"]["file"])
        parsed.main(payload["data"]["targets"])
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
