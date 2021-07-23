import copy
from dataclasses import dataclass, field
from distutils.version import LooseVersion
from typing import Dict, Union

from aziona.core import commands, io, text
from aziona.core.conf import errors, session, settings


@dataclass
class ParserOptionsStructure:
    interpolation: bool = True
    session_clean_before: bool = False
    session_clean_after: bool = False


@dataclass
class ParserTargetOptionsStructure:
    allow_failure_stage: list = field(default_factory=list)
    allow_failure_before: list = field(default_factory=list)
    allow_failure_after: list = field(default_factory=list)


@dataclass
class ParserStageStructure:
    module: str
    type: str
    args: Union[str, dict] = field(default_factory=dict)
    session: dict = field(default_factory=dict)
    before: dict = field(default_factory=dict)
    after: dict = field(default_factory=dict)


@dataclass
class ParserTargetStructure:
    stages: Dict[str, ParserStageStructure]
    env: dict = field(default_factory=dict)
    before: dict = field(default_factory=dict)
    after: dict = field(default_factory=dict)
    options: ParserTargetOptionsStructure = field(
        default_factory=ParserTargetOptionsStructure
    )


class ParserEgine(object):
    targets: Dict[str, ParserTargetStructure]
    options: ParserOptionsStructure = field(default_factory=ParserOptionsStructure)
    env: dict = field(default_factory=dict)
    version: LooseVersion = LooseVersion("1")

    def __init__(self, raw: dict):
        self.options = self._process_options(data=raw.get("options", {}))
        self.env = self._make_interpolation(data=raw.get("env", {}))
        self._process_targets(data=raw.get("targets", {}))

    def __str__(self) -> str:
        return str(self.__dict__)

    def _process_options(self, data: dict):
        return ParserOptionsStructure(**data)

    def _make_interpolation(self, data, from_dict: dict = {}):
        if self.options.interpolation is True:
            return text.interpolation_vars(data, from_dict)
        return data

    def _make_args(self, data) -> str:
        if isinstance(data, (str, bool, int, float)):
            return str(data)

        if isinstance(data, (list, tuple)):
            return " ".join([str(item) for item in data])

        # @TODO trovare medoto migliore
        if isinstance(data, dict):
            return " ".join(
                [
                    opt
                    + (" " if opt not in ["--action-args", "--jq-query"] else "='")
                    + (self._make_args(item) if item else "")
                    + ("" if opt not in ["--action-args", "--jq-query"] else "'")
                    for opt, item in data.items()
                ]
            )

        return ""

    def _process_targets(self, data: dict):
        def _process_target_stages(data: dict):
            def _copy_from(stage_name: str, stage_data: str):
                try:
                    cp_target_name, cp_stage_name = stage_data.split(".")
                except Exception as e:
                    io.exception(
                        e,
                        "Valore non corretto dello stage '%s': %s.\nFormato corretto: nome_target.nome_stage "
                        % (stage_name, stage_data),
                    )

                target = self.targets.get(cp_target_name, None)

                if target is None:
                    raise errors.CriticalError(
                        message="Target %s non trovato" % target_name
                    )

                if not target.stages.get(cp_stage_name, None):
                    raise errors.CriticalError(
                        message="Stage %s non trovato nel target %s"
                        % (cp_stage_name, cp_target_name)
                    )
                stage = copy.deepcopy(target.stages.get(cp_stage_name))

                return {stage_name: stage}

            def _make_from(stage_name: str, stage_data: dict):
                type = stage_data.get(
                    "type", settings.getconst("PARSER_INTERPRETER").get("default")
                )

                return {
                    stage_name: ParserStageStructure(
                        type=type,
                        module=stage_data.get("module"),
                        args=stage_data.get("args", ""),
                        session=stage_data.get("session", []),
                        before=stage_data.get("before", {}),
                        after=stage_data.get("after", {}),
                    )
                }

            stages = {}

            for stage_name, stage_data in data.items():
                if isinstance(stage_data, str):
                    stages.update(_copy_from(stage_name, stage_data))
                    continue

                if isinstance(stage_data, dict):
                    stages.update(_make_from(stage_name, stage_data))
                    continue

                raise errors.CriticalError(message="Stage %s non valido" % stage_name)

            return stages

        def _process_target_options(data: dict):
            return ParserTargetOptionsStructure(**data)

        def _process_target_env(data: dict):
            return {**self.env.copy(), **self._make_interpolation(data, self.env)}

        self.targets = {}
        for target_name, target_raw in data.items():
            target_options = _process_target_options(target_raw.get("options", {}))
            target_env = _process_target_env(target_raw.get("env", {}))
            target_stages = _process_target_stages(target_raw.get("stages"))
            target_before = self._make_interpolation(
                target_raw.get("before", {}), target_env
            )
            target_after = self._make_interpolation(
                target_raw.get("after", {}), target_env
            )
            self.targets[target_name] = ParserTargetStructure(
                stages=target_stages,
                options=target_options,
                env=target_env,
                before=target_before,
                after=target_after,
            )

    def _run(self, command: str, allow_failure: bool, env: dict = {}):
        try:
            io.debug("Esecuzione comando: %s" % command)
            commands.exec(command, env=settings.environ(**env))
        except Exception as e:
            message = "Options allow_failure: %s\nComando: %s\n%s" % (
                ("ATTIVO" if allow_failure else "DISATTIVO"),
                command,
                str(e),
            )
            if allow_failure is True:
                io.error(message)
            else:
                io.critical(message)

    def _exec_action(self, actions: dict, allow_failure, env: dict = {}):
        for act_name, act_value in actions.items():
            io.step("action: '%s'" % act_name, 1)
            if isinstance(allow_failure, list):
                allow_failure = act_name in allow_failure

            self._run(command=act_value, allow_failure=allow_failure, env=env)

    def _exec_stage(self, target: ParserTargetStructure):
        if not isinstance(target, ParserTargetStructure):
            pass

        for stage_name, stage_value in target.stages.items():
            io.step("Stage '%s'" % stage_name)

            # Caricamento sessione temporanea
            stage_session = {**target.env}
            for key in stage_value.session:
                stage_session.update(**session.get(key)[key])

            # Interpolazione dei valori usando l'env costruito ad-hoc per lo stage:
            # ENV HOST -> ENV .aziona.yml -> ENV TARGET .aziona.yml -> SESSIONE
            stage_module = self._make_interpolation(stage_value.module, stage_session)
            stage_args = self._make_args(
                self._make_interpolation(stage_value.args, stage_session)
            )
            stage_command = settings.const.get_interpreter(stage_value.type).format(
                module=stage_module, args=stage_args
            )
            stage_before = self._make_interpolation(stage_value.before, stage_session)
            stage_after = self._make_interpolation(stage_value.after, stage_session)
            self._exec_action(
                actions=stage_before,
                allow_failure=target.options.allow_failure_before,
                env=stage_session,
            )

            if isinstance(target.options.allow_failure_stage, list):
                allow_failure = stage_name in target.options.allow_failure_stage
            else:
                allow_failure = target.options.allow_failure_stage

            io.step("modulo: " + stage_value.module, 1)

            self._run(
                command=stage_command, allow_failure=allow_failure, env=stage_session
            )

            self._exec_action(
                actions=stage_after,
                allow_failure=target.options.allow_failure_after,
                env=stage_session,
            )

    def _clean_session(self, flag: bool):
        if flag is True:
            io.info("Session cleaned")
            session.clean()

    def main(self, *targets):
        self._clean_session(flag=self.options.session_clean_before)

        for name in targets:
            if name not in self.targets.keys():
                io.warning("Target %s non trovato nel template" % name)
                continue

            target = self.targets.get(name)

            self._exec_action(
                actions=target.before,
                allow_failure=target.options.allow_failure_before,
                env=target.env,
            )

            self._exec_stage(target)

            self._exec_action(
                actions=target.after,
                allow_failure=target.options.allow_failure_after,
                env=target.env,
            )

        self._clean_session(flag=self.options.session_clean_after)
