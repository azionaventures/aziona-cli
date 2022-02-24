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


def main(filename: str, targets: list) -> bool:
    try:
        schema = translator.Schema(filename=filename)

        from aziona.ingress import route

        settings.setenv_from_dict(overwrite=True, **schema.parser.env)

        for name in targets:
            target = schema.parser.targets.get(name, None)

            if target is None:
                io.warning(f"Target {name} not found in aziona file")
                continue

            data = {
                "stages": target.stages,
                "env": target.env,
                "options": target.options,
                "name": name,
            }
            r = route.get("runtime", data)
            r.run()
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
