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

from aziona.core import log
from aziona.core.conf import errors, settings


def std_input(message: str):
    """Standard input

    Args:
        message (str): Il messaggio che viene stampato a video

    Returns:
        str: Ritorna l'input digitato

    Raises:
        None
    """
    return input("+ %s " % message)


def confirm(message="Confermi:"):
    """Funzione per la conferma attraverso input

    Args:
        message (str): Il messaggio che viene stampato a video

    Returns:
        bool: Ritorna True se ha confermato, False se ha negato.

    Raises:
        Exception: se i valori inseriti in input non sono validi
    """
    yes = ["yes", "y", "si", "s"]
    no = ["no", "n"]
    choice = std_input(message + " (opzioni " + ",".join(yes + no) + "):").lower()
    if choice in yes:
        return True
    if choice in no:
        return False
    raise Exception("Inserrire %s oppure %s" % (yes, no))


@settings.verbose(level=3)
def debug(message):
    """Funzione per stampare le info di debug

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose.In automatico viene loggata la risposta.

    Args:
        message (str): Il messaggio che viene stampato a video e nel log

    Returns:
        void

    Raises:
        None
    """
    log.debug(message)
    print("[DEBUG] %s" % message)


@settings.verbose(level=2)
def info(message):
    """Funzione per stampare le info

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose.In automatico viene loggata la risposta.

    Args:
        message (str): Il messaggio che viene stampato a video e nel log

    Returns:
        void

    Raises:
        None
    """
    log.info(message)
    print("[INFO] %s" % message)


@settings.verbose(level=2)
def step(message: str, deep: int = 0):
    """Funzione per stampare gli avanzamenti

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose.In automatico viene loggata la risposta.

    Args:
        message (str): Il messaggio che viene stampato a video e nel log

    Returns:
        void

    Raises:
        None
    """
    log.info(message)
    print("[STEP]%s+-- %s" % (("\t" * deep), message))


@settings.verbose(level=2)
def warning(message):
    """Funzione per stampare i warning

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose.In automatico viene loggata la risposta.

    Args:
        message (str): Il messaggio che viene stampato a video e nel log

    Returns:
        void

    Raises:
        None
    """
    log.warning(message)
    print("[WARNING] %s" % message)


@settings.verbose(level=1)
def response(message):
    """Funzione per stampare le risposte

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose.In automatico viene loggata la risposta.

    Args:
        message (str): Il messaggio che viene stampato a video e nel log

    Returns:
        void

    Raises:
        None
    """
    log.info(message)
    print("[RESPONSE] %s" % message)


@settings.verbose(level=1)
def error(message: str):
    """Funzione per stampare errori

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose.In automatico viene loggata la risposta.

    Args:
        message (str): Il messaggio che viene stampato a video e nel log

    Returns:
        void

    Raises:
        Exception: Indica l'errore
    """
    log.error(message)
    print("[ERROR] %s" % message)


@settings.verbose(level=1)
def critical(message: str):
    """Funzione per stampare errori critici

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose. In automatico viene loggata la risposta.
    In automatico effettua il raise e bloccando l'esecuzione

    Args:
        message (str): Il messaggio che viene stampato a video e nel log

    Returns:
        void

    Raises:
        Exception: Indica l'errore
    """
    try:
        raise errors.CriticalError(message=message)
    except Exception as e:
        exception(e, with_traceback=False)


@settings.verbose(level=1)
def exception(
    exception: Exception,
    message: str = None,
    exitcode: int = 1,
    with_traceback: bool = True,
):
    """Funzione per stampare le eccezzioni

    Viene eseguita solo se soddisfa le condizioni del decoratore @verbose.In automatico viene loggata la risposta.

    Args:
        exception (exceptions): L'eccezzione cattorata nel except
        message (str,optional): Il messaggio aggiuntivo
        exitcode (int,optional): Il numero intero con cui terminare il programma
        with_traceback (bool,optional): Se true stampa a video il traceback dell'errore

    Returns:
        void

    Raises:
        None
    """

    def func(exception: Exception, message: str, exitcode: int, with_traceback: bool):
        log.exception(message)
        print("[EXCEPTION] %s\n%s" % (message, str(exception)))

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
        return "".join(self)

    def json(self):
        return json.dumps(self.__str__())
