
class RuntimeBaseClass():
    interpreter: str = None
    env: dict = None
    args: dict = None
    options: dict = None

    def __init__(self, interpreter: str, env: dict = None, args: dict = None, options: dict = None) -> None:
        self.interpreter = interpreter
        self.env = env or {}
        self.args = args or {}
        self.options = options or {}

    def exec(self):
        raise NotImplementedError()

    def _make_args(self, data) -> str:
        if isinstance(data, (str, bool, int, float)):
            return str(data)

        if isinstance(data, (list, tuple)):
            return ' '.join([str(item) for item in data])

        # @TODO trovare medoto migliore
        if isinstance(data, dict):
            return ' '.join(
                [
                    opt
                    + (' ' if opt not in ['--action-args', '--jq-query'] else "='")
                    + (self._make_args(item) if item else '')
                    + ('' if opt not in ['--action-args', '--jq-query'] else "'")
                    for opt, item in data.items()
                ]
            )

        return ''
