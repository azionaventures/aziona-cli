from dataclasses import dataclass, field

from aziona.services.utilities import commands, io


@dataclass
class _BaseClass:
    action: str
    interpreter: str
    env: dict = field(default_factory=dict)
    args: dict = field(default_factory=dict)
    options: dict = field(default_factory=dict)

    def run(self):
        raise NotImplementedError()

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


@dataclass
class Python(_BaseClass):
    interpreter: str = "python3"

    def run(self):
        command = f"{self.interpreter} -m {self.action} {self._make_args(self.args)}"
        try:
            io.debug("Esecuzione comando: %s" % command)
            commands.exec(command, env=self.env)
        except Exception as e:
            print(e)
            # message = "Options allow_failure: %s\nComando: %s\n%s" % (
            #    ("ATTIVO" if allow_failure else "DISATTIVO"),
            #    command,
            #    str(e),
            # )
            # if allow_failure is True:
            #    io.error(message)
            # else:
            #    io.critical(e)
