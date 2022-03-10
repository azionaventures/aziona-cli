from aziona.services.utilities import commands, io
from aziona.services.runtime import RuntimeBaseClass


class Python(RuntimeBaseClass):
    module: str

    def __init__(self, module: str, type: str, env: dict = None, args: dict = None, options: dict = None) -> None:
        super().__init__('python3', type, env, args, options)
        self.module = module

    def exec(self):
        command = f'{self.interpreter} -m {self.module} {self._make_args(self.args)}'
        try:
            io.debug('Esecuzione comando: %s' % command)
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
