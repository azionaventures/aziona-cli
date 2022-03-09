from dataclasses import dataclass, field

from aziona import errors
from aziona.ingress import runtime, targets

IN_V1_TARGETS = 'targets'
IN_V1_RUNTIME = 'runtime'

routes = {
    'targets': {
        'module': targets,
        'properties': targets.__VALIDATOR__PROP__.keys(),
        'validate': targets.validate,
    },
    'runtime': {
        'module': runtime,
        'properties': runtime.__VALIDATOR__PROP__.keys(),
        'validate': runtime.validate,
    },
}


@dataclass
class Dispatcher:
    @dataclass
    class _Payload:
        index: str
        data: list = field(default_factory=dict)

    module: object = None
    validate: object = None
    properties: list = field(default_factory=dict)
    payload: _Payload = field(default_factory=_Payload)

    def is_valid(self):
        self.validate(self.payload['data'])

    def run(self):
        self.is_valid()
        self.module.main(**self.payload['data'])


def get_ingress(index: str, data: dict):
    route = routes.get(index, {}).copy()
    if not route:
        raise errors.CriticalError(message=f'Route {index} not found')

    route.update(payload={'index': index, 'data': data})

    return Dispatcher(**route)
