# -*- coding: utf-8 -*-
import argparse

from aziona import errors, settings
from aziona.services.utilities import text


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
        settings.setenv("AZIONA_VERBOSITY", 2, overwrite=True)
        setattr(namespace, self.dest, 2)


class StoreVerbosityPreset3Parser(argparse.Action):
    """Argparse per settare la verbosity

    Attributes:
        None
    """

    def __call__(self, parser, namespace, values, option_string=None):
        settings.setenv("AZIONA_VERBOSITY", 3, overwrite=True)
        setattr(namespace, self.dest, 3)


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
        choices=[1, 2, 3],
        action=StoreVerbosityParser,
        default=1,
        type=int,
        help="Verbosity level",
    )

    return parser
