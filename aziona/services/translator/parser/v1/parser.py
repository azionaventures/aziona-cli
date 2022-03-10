from dataclasses import dataclass, field
from typing import Dict, List, Union
import fastjsonschema

from packaging import version

from aziona.services.translator.parser import BaseParserEgine, MapStructure
from aziona.services.utilities import text

VERSION = version.parse('1.0')


RuntimeValidator = {
    'python': {
        'type': 'object',
        'properties': {
            'module': {'type': 'string'}
        },
    }
}


@dataclass
class RepeatStructure:
    count: int = 1
    sleep: float = 0.0


@dataclass
class OptionsStructure:
    @dataclass
    class _SessionStructure:
        class _CleanStructure:
            before: bool = False
            after: bool = False

        clean: _CleanStructure = field(default_factory=_CleanStructure)

    @dataclass
    class _FailureStructure:
        type: str = field(default_factory=str)
        threshold: str = field(default_factory=str)
        name: dict = field(default_factory=dict)

    failure: List[_FailureStructure] = field(default_factory=list)
    interpolation: bool = True
    session: _SessionStructure = field(default_factory=_SessionStructure)
    repeat: RepeatStructure = field(default_factory=RepeatStructure)


@dataclass
class StageStructure:
    type: str
    runtime: dict = field(default_factory=dict)
    env: dict = field(default_factory=dict)
    args: Union[str, dict] = field(default_factory=dict)
    session: dict = field(default_factory=dict)
    repeat: RepeatStructure = field(default_factory=RepeatStructure)


@dataclass
class TargetStructure:
    stages: Dict[str, MapStructure] = field(default_factory=MapStructure)
    options: MapStructure = field(default_factory=MapStructure)
    env: MapStructure = field(default_factory=MapStructure)


class ParserEngine(BaseParserEgine):
    targets: MapStructure
    env: MapStructure
    options: OptionsStructure
    version: str

    def run(self):
        self.version = VERSION

        self.options = OptionsStructure(**self._raw.get('options', {}))

        if self.options.interpolation is True:
            self.env = MapStructure(text.interpolation(self._raw.get('env', {})))
        else:
            self.env = MapStructure(self._raw.get('options', {}))

        self.targets = MapStructure({})
        for target_name, target_data in self._raw.targets.items():
            if target_data.get('options', {}).get('interpolation', True):
                env = MapStructure(
                    text.interpolation(target_data.get('env', {}), self.env)
                )

            stages = {}
            for stage_name, stage_data in target_data.get('stages', {}).items():
                # validate = fastjsonschema.compile(RuntimeValidator.get(stage_data["type"]))
                # validate(stage_data["runtime"])

                stages[stage_name] = StageStructure(
                    **text.interpolation(stage_data, env)
                )

            self.targets[target_name] = TargetStructure()

            if stages:
                self.targets[target_name].stages = MapStructure(stages)

            if env:
                self.targets[target_name].env = MapStructure(env)

            self.targets[target_name].options = MapStructure(
                OptionsStructure(**target_data.get('options', {})).__dict__
            )

        print(self.targets)
