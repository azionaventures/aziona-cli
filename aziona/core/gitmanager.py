# -*- coding: utf-8 -*-
"""Il modulo repository.py contiene funzioni e classi per gestire le operazioni di git versionig.
"""
import os

import git

from aziona.core import files, io


def init(project_path):
    """Inizializzazione progetto

    Args:
        project_path (str): Path del progetto da inizializzare

    Returns:
        git.Repo: istanza del progetto

    Raises:
        GitError: errori derivanti dalla libreria git
        Exception: errori generici
    """
    try:
        return git.Repo.init(project_path)
    except git.GitError as e:
        io.exception(e, "Errore funzione git.Repo.init(..)")
    except Exception as e:
        io.exception(e)


def push(project_path, opt=""):
    """Push dei commit

    Args:
        project_path(str): Path del progetto da inizializzare
        opt(str,optional): Opzioni da passare al comando push

    Returns:
        None

    Raises:
        GitError: errori derivanti dalla libreria git
        Exception: errori generici
    """
    try:
        gitobj = git.Repo(project_path)

        gitobj.remote().push(opt)
    except git.GitError as e:
        io.exception(e, "Errore funzione git.Repo(..).remote().push(..)")
    except Exception as e:
        io.exception(e)


def commit(project_path, message, add=""):
    """Creazione del commit

    Args:
        project_path(str): Path del progetto da inizializzare
        message(str): Messaggio del commit
        add(str,optional): Consente di specificare cosa aggiungere al commit, ex. "."

    Returns:
        None

    Raises:
        GitError: errori derivanti dalla libreria git
        Exception: errori generici
    """
    try:
        gitobj = git.Repo(project_path)
        gitobj.remote().fetch()

        if add:
            gitobj.git.add(add)

        gitobj.git.commit(m=message)
    except git.GitError as e:
        io.exception(e, "Errore funzione git")
    except Exception as e:
        io.exception(e)


def clone(name, path, url, source=None):
    """Clone di un progetto

    Args:
        name(str): nome del progetto
        path(str): Path base dove scaricare il progetto
        url(str): Url del sorgente da scaricare
        source(str,optional): Effettua il checkout in un branch

    Returns:
        None

    Raises:
        GitError: errori derivanti dalla libreria git
        Exception: errori generici
    """
    try:
        dirpath = files.generate_path(path, name)

        if not os.path.isdir(dirpath):
            git.Git(path).clone(url)

        gitobj = git.Repo(dirpath)
        gitobj.remote().fetch()

        if source is not None:
            try:
                gitobj.git.checkout(source)
            except Exception:
                gitobj.git.checkout(b=source)

        if not os.path.exists(path):
            raise git.NoSuchPathError(path)

        return gitobj
    except git.NoSuchPathError as e:
        io.exception(e)
    except git.GitError as e:
        io.exception(e, "Errore funzione git")
    except Exception as e:
        io.exception(e)


def checkout(repo_path, branch_name, gitobj=None):
    try:
        repo = git.Repo(repo_path) if gitobj is None else gitobj
        repo.git.checkout(branch_name)
    except repo.exc.GitCommandError as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
