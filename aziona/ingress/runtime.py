import sys

import fastjsonschema

from aziona.services.utilities import io

__VALIDATOR__PROP__ = {
    "name": {"type": "string", "default": ""},
    "stages": {"type": "object", "default": {}},
    "env": {"type": "object", "default": {}},
    "options": {"type": "object", "default": {}},
}

validate = fastjsonschema.compile(
    {
        "type": "object",
        "properties": __VALIDATOR__PROP__,
    }
)


def main(payload) -> bool:
    try:
        print(payload)
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
