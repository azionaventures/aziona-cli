import sys
from time import sleep

import fastjsonschema

from aziona.services import runtime
from aziona.services.utilities import io

__VALIDATOR__PROP__ = {
    'name': {'type': 'string', 'default': ''},
    'stages': {'type': 'object', 'default': {}},
    'env': {'type': 'object', 'default': {}},
    'options': {'type': 'object', 'default': {}},
}

validate = fastjsonschema.compile(
    {
        'type': 'object',
        'properties': __VALIDATOR__PROP__,
    }
)


def main(name: str, stages: object, env: object = {}, options: object = {}) -> bool:
    try:
        io.info(f'Run {name} target')
        io.debug(f'Target env: {env}', 1)
        io.debug(f'Target opitons: {options}', 1)

        for repeat in range(options.repeat.count):
            for name, stage in stages.items():
                io.info(f'Run {name} stage', 1)
                io.debug(f'Stage data: {stage}', 1)

                import os

                r = runtime.get('python')(
                    action=stage.action,
                    env={**os.environ, **env, **stage.env},
                    args=stage.args,
                    options=options,
                )

                r.run()
            sleep(options.repeat.sleep)
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
