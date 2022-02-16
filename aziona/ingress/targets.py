import sys

import fastjsonschema

from aziona import settings
from aziona.services.translator import translator
from aziona.services.utilities import io

__VALIDATOR__PROP__ = {
    "filename": {"type": "string", "default": settings.TEMPLATE_FILE_NAME},
    "targets": {"type": "array", "default": []},
}

validate = fastjsonschema.compile(
    {
        "type": "object",
        "properties": __VALIDATOR__PROP__,
    }
)


def main(payload) -> bool:
    try:
        schema = translator.Schema(filename=payload["data"]["filename"])
        print(schema.parser)
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
