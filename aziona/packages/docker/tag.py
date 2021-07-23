# -*- coding: utf-8 -*-

import sys

from aziona.core import argparser, commands, io


def argsinstance():
    parser = argparser.argparse.ArgumentParser()
    parser.add_argument(
        "--tag-from",
        required=True,
        default=None,
        type=str,
        help="A tag from create new tag",
    )
    parser.add_argument(
        "--tag-to",
        required=True,
        default=None,
        type=str,
        nargs="+",
        help="New tags created from another tag",
    )
    argparser.standard_args(parser)

    return parser


def load(args) -> None:
    """Esegue la logica del modulo.

    Args:
        args(dict,argparse.Namespace,optional): argomenti richiesti dal modulo

    Returns:
        None:
    """
    if isinstance(args, dict):
        args = argparser.namespace_from_dict(argsinstance()._actions, args)

    if not isinstance(args, argparser.argparse.Namespace):
        io.critical("Argomenti non validi")

    for tag in args.tag_to:
        commands.exec("docker tag %s %s" % (args.tag_from, tag))


def main() -> bool:
    try:
        load(args=argsinstance().parse_args())
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
