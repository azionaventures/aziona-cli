# -*- coding: utf-8 -*-
"""Il modulo io.py gestisce ogni input/output consentendo di uniformare e standardizzare le interazioni. \
Tutte le funzioni di output scrivono nel log, usando rispettivamente il livello della funzione di output, \
il log viene scritto solo se effettivamente la funzione viene eseguita. \
Le funzioni di output sono poste sotto controllo della verbosità, il che vuol dire che l'output viene \
eseguita solo se il grado di verbose (indicato all'esecuzione o quello di default) è uguale o maggiore \
a quello richiesto dalla funzione di print. \

- debug: richiede verbosity 3
- info: richiede verbosity 2
- warning: richiede verbosity 2
- error: richiede verbosity 1
- critical: richiede verbosity 1
- exception: richiede verbosity 1
"""

import json
import sys
from io import StringIO

from aziona import errors, settings
from aziona.services.utilities import log


def get_verbosity_level():
    if settings.VERBOSITY in settings.VERBOSITY_LVL:
        return settings.VERBOSITY
    return settings.VERBOSITY_DEFAULT_LVL


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
                func(*args, **kwargs) if level <= int(settings.VERBOSITY) else neutered
            )

        return wrapper

    return actual_decorator


def std_input(message: str):
    """Standard input

    Args:
        message (str): Il messaggio che viene stampato a video

    Returns:
        str: Ritorna l'input digitato

    Raises:
        None
    """
    return input('+ %s ' % message)


def confirm(message='Confermi:'):
    """Funzione per la conferma attraverso input

    Args:
        message (str): Il messaggio che viene stampato a video

    Returns:
        bool: Ritorna True se ha confermato, False se ha negato.

    Raises:
        Exception: se i valori inseriti in input non sono validi
    """
    yes = ['yes', 'y', 'si', 's']
    no = ['no', 'n']
    choice = std_input(message + ' (opzioni ' + ','.join(yes + no) + '):').lower()
    if choice in yes:
        return True
    if choice in no:
        return False
    raise Exception('Inserrire %s oppure %s' % (yes, no))


@verbose(level=3)
def debug(message: str, deep: int = 0):
    log.debug(message)
    lvl = '[DEBUG]'
    if deep > 0:
        lvl = ('\t|___ ' * deep) + lvl
    print(f'{lvl} {message}')


@verbose(level=2)
def info(message: str, deep: int = 0):
    log.info(message)
    lvl = '[INFO]'
    if deep > 0:
        lvl = ('\t|___ ' * deep) + lvl
    print(f'{lvl} {message}')


@verbose(level=2)
def warning(message, deep=0):
    log.warning(message)
    lvl = '[WARN]'
    if deep > 0:
        lvl = ('\t|___ ' * deep) + lvl
    print(f'{lvl} {message}')


@verbose(level=1)
def response(message: str, deep: int = 0):
    log.info(message)
    lvl = '[RESPONSE]'
    if deep > 0:
        lvl = ('\t|___ ' * deep) + lvl
    print(f'{lvl} {message}')


@verbose(level=1)
def error(message: str, deep: int = 0):
    log.error(message)
    lvl = '[ERROR]'
    if deep > 0:
        lvl = ('\t|___ ' * deep) + lvl
    print(f'{lvl} {message}')


@verbose(level=1)
def critical(message: str):
    try:
        raise errors.CriticalError(message=message)
    except Exception as e:
        exception(e, with_traceback=False)


@verbose(level=1)
def exception(
    exception: Exception,
    message: str = None,
    exitcode: int = 1,
    with_traceback: bool = True,
):
    def func(exception: Exception, message: str, exitcode: int, with_traceback: bool):
        log.exception(message)
        print('[EXCEPTION] %s\n%s' % (message, str(exception)))

        if with_traceback is True:
            import traceback

            print(traceback.format_exc())

        sys.exit(exitcode if isinstance(exitcode, int) else 1)

    try:
        if not isinstance(exception, Exception):
            raise errors.ExcpetionNotValidError(exception=str(exception))
    except Exception as e:
        exception = e

    func(exception, message, exitcode, with_traceback)


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout

    def __str__(self):
        return ''.join(self)

    def json(self):
        return json.dumps(self.__str__())
