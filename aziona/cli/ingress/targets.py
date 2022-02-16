import sys

import fastjsonschema

from aziona.services.drivers import executor
from aziona.services.utilities import io

__VALIDATOR__PROP__ = {
    "filename": {"type": "string", "default": ".aziona.yml"},
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
        executor.main(**payload["data"])
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
