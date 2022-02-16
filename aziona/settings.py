import os

from aziona import __version__

NAME = "aziona"

VERSION = __version__

VERBOSITY_DEFAULT_LVL = 1
VERBOSITY_LVL = (1, 2, 3)
VERBOSITY = os.getenv("AZIONA_VERBOSITY", VERBOSITY_DEFAULT_LVL)

AZIONA_PATH = os.getenv("AZIONA_PATH", os.environ["HOME"] + "/.aziona")

TEMPLATE_FILE_NAME = os.getenv("AZIONA_TEMPLATE_FILENAME", ".aziona.yml")

LOGGING_NAME = os.getenv("AZIONA_LOGGING_NAME", "main")

LOGGING_PATH = os.getenv("AZIONA_LOGGING_PATH", f"{AZIONA_PATH}/logs")

LOGGING_FORMAT = os.getenv(
    "AZIONA_LOGGING_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

RUNTIME_ENV = {}


def get_verbosity_level():
    if VERBOSITY in VERBOSITY_LVL:
        return VERBOSITY
    return VERBOSITY_DEFAULT_LVL


def setenv(key: str, value: str, overwrite: bool = False) -> None:
    """Caricamento di una nuova variabile di ambiente

    Args:
        key (str): Nome variabili d'ambiente
        value (str): Valore
        overwrite (bool,optional): Overwrite variabile d'ambiente se esiste già

    Returns:
        None
    """
    if not isinstance(key, str):
        raise Exception("ENVIRON KEY is not str")

    if not isinstance(value, str):
        value = str(value)

    key = key.upper()

    if key in os.environ.keys() and overwrite is False:
        return

    globals()["RUNTIME_ENV"].update({key: value})

    os.environ[key] = value


def setenv_from_dict(overwrite: bool = False, **kargs) -> None:
    """Caricamento varibili di ambiente a partire da un dict.

    Se il valore è un dict verrà caricato con la chiave principale seguita dalla secondaria, KEY_KEYCHILD=VALUECHILD.
    Ex. {test:{subtest:'ok'}} => TEST_SUBTEST=ok

    Args:
        overwrite (bool,optional): Overwrite variabile d'ambiente se esiste già
        **kargs: chiave=valore

    Returns:
        None
    """
    for key, value in kargs.items():
        if isinstance(kargs[key], str):
            setenv(key, value, overwrite)
            continue

        if isinstance(kargs[key], dict):
            [setenv(key + "_" + k, v, overwrite) for k, v in kargs[key].items()]

        raise Exception("Errore caricamento env %s=%s"(key, str(value)))


def verbose(level: str):
    """DECORATORE - Utilizzato per wrappare le funzioni di i/o

    Consente alla funzione wrappata di essere eseguita o no in base al livello di verbosity indicato.
    Se il livello richiesto è >= a quello restituito dalla funzione get_verbosity_level() la funzione verrà eseguita.
    Se il livello è minore verrà ignorata.

    Args:
        level (int): Indica il livello in cui la funzione può essere eseguita.

    Returns:
        function: Ritorna la funzione wrappata se soddisfa le condizioni di verbosity, sennò torna una funzione vuota.
    """
    import functools

    def actual_decorator(func):
        def neutered(*args, **kw):
            return

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) if level <= get_verbosity_level() else neutered

        return wrapper

    return actual_decorator
