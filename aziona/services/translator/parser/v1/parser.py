from dataclasses import dataclass, field
from typing import Dict, List, Union

from packaging import version

from .. import BaseParserEgine

VERSION = version.parse("1.0")


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

    failure: List[_FailureStructure]
    interpolation: bool = True
    session: _SessionStructure = field(default_factory=_SessionStructure)
    repeat: RepeatStructure = field(default_factory=RepeatStructure)


@dataclass
class StageStructure:
    action: str
    runtime: str
    args: Union[str, dict] = field(default_factory=dict)
    session: dict = field(default_factory=dict)
    repeat: RepeatStructure = field(default_factory=RepeatStructure)


@dataclass
class TargetStructure:
    stages: Dict[str, StageStructure]
    env: dict = field(default_factory=dict)
    options: OptionsStructure = field(default_factory=OptionsStructure)


class ParserEngine(BaseParserEgine):
    targets: Dict[str, TargetStructure]
    options: OptionsStructure = field(default_factory=OptionsStructure)
    env: dict = field(default_factory=dict)
    version: VERSION
