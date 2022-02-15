# -*- coding: utf-8 -*-
"""Il modulo commands.py espone le funzionalità per l'esecuzione di comandi esterni al programma.

Consente l'esecuzione di comandi in base all'OS host.
"""

import shlex
import subprocess


def exec_check(command, **kargs) -> None:
    """Esegue un comando attraverso il subprocess

    Args:
        command(str,dict): il comando da eseguire
        **kargs(dict): opzioni del comando subprocess.check_call

    Returns:
        void

    Raises:
        Exception generiche
    """
    if isinstance(command, str):
        command = shlex.split(command)

    try:
        if not isinstance(command, list):
            raise Exception(
                "Il comando non è valido, deve essere una stringa o una lista"
            )
        return subprocess.check_call(command, **kargs)
    except IOError as e:
        if e[0] == "errno.EPERM":
            raise Exception(str(e) + "Non hai i permessi di amministratore.")
        raise Exception(str(e))
    except Exception as e:
        raise Exception(str(e))


def exec(command: str, shell: bool = True, **kargs) -> object:
    """Esegue un comando attraverso il subprocess per recuperare il processo eseguito

    Args:
        command (str): il comando da eseguire
        shell (bool,optional): opzione subprocess
        **kargs(dict): opzioni del comando subprocess.check_call

    Returns:
        object

    Raises:
        Exception
    """
    p = subprocess.run(command, stderr=subprocess.PIPE, shell=shell, **kargs)
    if p.returncode != 0:
        raise Exception(p.stderr.decode())
    return p


def exec_output(
    command: str,
    shell: bool = True,
    with_raise: bool = True,
    decode: bool = True,
    **kargs
) -> str:
    """Esegue un comando attraverso il subprocess per recuperare il suo output in formato stringa

    Args:
        command (str): il comando da eseguire
        shell (bool,optional): opzione subprocess
        with_raise (bool,optional): se true cattura l'eccezione se false ritorna la stringa dell'errore
        decode (bool,optional): decodifica l'output
        **kargs(dict): opzioni del comando subprocess.check_call

    Returns:
        str: output del comando eseguito

    Raises:
        Exception
    """
    try:
        response = subprocess.check_output(command, shell=shell, **kargs)
        return response.decode().replace("\n", "") if decode is True else response
    except subprocess.CalledProcessError as e:
        if with_raise is False:
            return e.stderr
        raise e
