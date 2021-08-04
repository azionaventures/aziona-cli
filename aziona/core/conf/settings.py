import os
from datetime import datetime
from distutils.version import LooseVersion

from aziona.core.conf import const

DEFAULT = {
    "AZIONA_TEMPLATE_FILE_NAME": ".aziona.yml",
    "AZIONA_VERBOSITY": "1",
    "AZIONA_TERRAFORM_TEMPLATE_PATH": "/opt/aziona-cli/terraform",
    "AZIONA_SESSION_FILENAME": "/tmp/aziona-session",
    "AZIONA_LOGGING_NAME": "main",
    "AZIONA_LOGGING_PATH": os.environ["HOME"] + "/.aziona/logs",
    "AZIONA_LOGGING_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "AZIONA_DATA": str(datetime.now().strftime("%Y-%m-%d")),
    "AZIONA_DATATIME_START": str(datetime.now().strftime("%Y-%m-%d %H:%m:%s")),
}


RUNTIME_ENV = {}


def getconst(key: str = None, default=None):
    return const.getconst(key, default)


def environ(**kargs: str) -> dict:
    """Restituisce l'ambiente dell'intero processo run-time, unendo:

        1. os.environ
        2. aziona.core.conf.config (solo ed esclusivamente i valore stringa)
        3. gli argomenti passati alla funzione
    Args:
        **kargs(str): valori da aggiungere all'environ
    Returns:
        dict: environ completo
    """
    # Recupera le varibili env del processo
    environ = {**os.environ.copy()}

    # Recupera i valori degli argomenti
    for key, value in kargs.items():
        if isinstance(value, str):
            environ[key] = value

    return environ


def getenv(key: str, default=None) -> str:
    return environ().get(key, default)


def get_data() -> str:
    return getenv(key="AZIONA_DATA")


def get_execution_start() -> str:
    return getenv(key="AZIONA_DATATIME_START")


def get_logging_basepath() -> str:
    return getenv(key="AZIONA_LOGGING_PATH")


def get_logging_format() -> str:
    return getenv(key="AZIONA_LOGGING_FORMAT")


def get_logging_name() -> str:
    return getenv(key="AZIONA_LOGGING_NAME")


def get_logging_filepath() -> str:
    return get_logging_basepath() + "/" + get_logging_name() + "-" + get_data() + ".log"


def get_logging_level() -> list:
    return ["info", "warning", "error", "debug", "critical", "exception"]


def get_aziona_template_name() -> str:
    return getenv("AZIONA_TEMPLATE_FILE_NAME")


def get_terraform_template_path() -> str:
    return getenv("AZIONA_TERRAFORM_TEMPLATE_PATH")


def get_aziona_template_path() -> str:
    return getenv("AZIONA_TEMPLATE_PATH")


def get_session_path(session_filepath: str = None) -> str:
    return session_filepath or getenv("AZIONA_SESSION_FILENAME")


def get_verbosity_level() -> LooseVersion:
    """Recupera il livello di verbosità del modulo.

    Il valore che ritorna è quello che il modulo ha in quell'instante.

    Args:
        None

    Returns:
        int: The return value. Level of verbosity

    Raises:
        None
    """
    value = getenv("AZIONA_VERBOSITY")

    if value in getconst("VERBOSITY_LEVEL"):
        return LooseVersion(value)

    return LooseVersion(DEFAULT["AZIONA_VERBOSITY"])


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

    if key in environ().keys() and overwrite is False:
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
            return (
                func(*args, **kwargs)
                if LooseVersion(str(level)) <= get_verbosity_level()
                else neutered
            )

        return wrapper

    return actual_decorator


####
# LOAD DEFAULT ENV
####
setenv_from_dict(overwrite=False, **DEFAULT)
