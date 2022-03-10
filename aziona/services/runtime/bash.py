from aziona.services.utilities import commands, io
from aziona.services.runtime import RuntimeBaseClass


class Bash(RuntimeBaseClass):
    script: str

    def __init__(self, script: str, env: dict = None, args: dict = None, options: dict = None) -> None:
        super().__init__('', env, args, options)
        self.script = script

    def exec(self):
        command = f'{self.interpreter} {self.script} {self._make_args(self.args)}'
        try:
            io.debug('Esecuzione comando: %s' % command)
            commands.exec(command, env=self.env)
        except Exception as e:
            print(e)
