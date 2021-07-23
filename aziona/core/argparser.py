# -*- coding: utf-8 -*-
"""Il modulo argparse.py contiene funzioni di utilità per il modulo base argparse"""

import argparse
import shlex

from aziona.core import text
from aziona.core.conf import errors, session, settings


class StoreDictParser(argparse.Action):
    """Struttura argparse.Action che consete ad un'opzione del parser di prendere in input un dizionario

    Ex. python -m xyz --opt a=1,b=2,c=ciao

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        data = {}
        for kv in values.split(","):
            k, v = kv.split("=")
            data[k] = v
        setattr(namespace, self.dest, data)


class StoreEnvParser(StoreDictParser):
    """Struttura argparse.Action che consete di convertire una stringa con caratteri speciali, usata per le password

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        super(StoreEnvParser, self).__call__(parser, namespace, values, option_string)
        settings.setenv_from_dict(overwrite=True, **namespace.env)


class StoreSessionLoadParser(argparse.Action):
    """Struttura argparse.Action che consete di caricare una o più chiavi dalla sessione condivisa

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        for session_name in values:
            session.load(key=session_name)


class StoreActionArgsParser(argparse.Action):
    """Struttura argparse.Action che consete di creare una lista comandi

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        data = []
        for item in values:
            data += shlex.split(item)
        setattr(namespace, self.dest, data)


class StoreSpecialStrParser(argparse.Action):
    """Struttura argparse.Action che consete di convertire una stringa con caratteri speciali, usata per le password

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, text.str_to_sysencoding(values))


class StoreVerbosityParser(argparse.Action):
    """Argparse per settare la verbosity

    Attributes:
        None
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(StoreVerbosityParser, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        settings.setenv("AZIONA_VERBOSITY", values, overwrite=True)
        setattr(namespace, self.dest, values)


class StoreVerbosityPreset2Parser(argparse.Action):
    """Argparse per settare la verbosity

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        settings.setenv("AZIONA_VERBOSITY", "2", overwrite=True)
        setattr(namespace, self.dest, values)


class StoreVerbosityPreset3Parser(argparse.Action):
    """Argparse per settare la verbosity

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        settings.setenv("AZIONA_VERBOSITY", "3", overwrite=True)
        setattr(namespace, self.dest, values)


class StoreParserVersionParser(argparse.Action):
    """Argparse per scegliere la versione del parser

    Attributes:
        None
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(StoreParserVersionParser, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            settings.setenv("PARSER_VERSION_DEFAULT", values)
        setattr(namespace, self.dest, values)


def namespace_from_dict(parser_actions: list, args_dict: dict):
    """Crea il namespace dell'argparse"""
    args = {}
    default_actions = ["help", "env", "env_form", "verbosity"]

    for action in parser_actions:
        # esclude le opzioni di default
        if action.dest in default_actions:
            continue

        if action.dest not in args_dict.keys():
            if action.required is True:
                raise Exception("Arg %s required" % action.dest)
            args[action.dest] = action.default
        else:
            if isinstance(action.type, type(args_dict[action.dest])):
                raise Exception("Arg %s invalid type" % action.dest)
            args[action.dest] = args_dict[action.dest]

    return argparse.Namespace(**args)


def verbosity_args(parser: object) -> object:
    if not isinstance(parser, argparse.ArgumentParser):
        raise errors.ParamTypeError(param="parser", type="argparse.ArgumentParser")

    parser.add_argument(
        "-v",
        action=StoreVerbosityPreset2Parser,
        type=str,
        nargs=0,
        help="Verbosity level",
    )

    parser.add_argument(
        "-vv",
        action=StoreVerbosityPreset3Parser,
        type=str,
        nargs=0,
        help="Verbosity level",
    )

    parser.add_argument(
        "--verbosity",
        choices=["1", "2", "3"],
        action=StoreVerbosityParser,
        default="1",
        type=str,
        help="Verbosity level",
    )

    return parser


def standard_args(parser: object) -> object:
    """Aggiunge all'oggetto parser argomenti comuni:

        - verbosity -> per settare la verobisty
        - env -> per aggiungere key=value all'environment del programma

    Args:
        parser (argparse.ArgumentParser): istanza argparse

    Returns:
        argparse.ArgumentParser: parser
    """
    if not isinstance(parser, argparse.ArgumentParser):
        raise errors.ParamTypeError(param="parser", type="argparse.ArgumentParser")

    parser = verbosity_args(parser)

    parser.add_argument(
        "-e",
        "--env",
        action=StoreEnvParser,
        default={},
        help="Consente di aggiungere variabili all'env. Accetta key=value (ex. TEST=123)",
    )

    parser.add_argument(
        "--session-load",
        action=StoreSessionLoadParser,
        nargs="+",
        default=[],
        type=str,
        help="Consente di aggiungere variabili all'env da file contenenti key/value",
    )

    parser.add_argument(
        "--session-save",
        default=None,
        type=str,
        help="Consente di salvare l'output del modulo nella sessione",
    )

    return parser


def action_args(parser):
    if not isinstance(parser, argparse.ArgumentParser):
        raise errors.ParamTypeError(param="parser", type="argparse.ArgumentParser")

    parser.add_argument(
        "--action-args",
        action=StoreActionArgsParser,
        default=[],
        nargs="+",
        type=str,
        help="Aws command options/args",
    )

    return parser


def jq_args(parser: object) -> object:
    if not isinstance(parser, argparse.ArgumentParser):
        raise errors.ParamTypeError(param="parser", type="argparse.ArgumentParser")

    parser.add_argument("--xargs", default=False, action="store_true", help="xargs")
    parser.add_argument(
        "--jq-query",
        action=StoreActionArgsParser,
        default=[],
        nargs="+",
        type=str,
        help="JQ query",
    )

    return parser
