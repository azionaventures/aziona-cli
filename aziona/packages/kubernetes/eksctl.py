# -*- coding: utf-8 -*-
"""Modulo per eseguire il comando eksctl
"""
import sys

from aziona.core import argparser, commands, io, text
from aziona.core.conf import session


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument("--action", required=True, type=str, help="Aws cli commands")

    argparser.standard_args(parser)
    argparser.action_args(parser)
    argparser.jq_args(parser)

    return parser


def load(args) -> None:
    """Esegue la logica del modulo.
    Args:
        args(dict,argparse.Namespace,optional): argomenti richiesti dal modulo
    Returns:
        None:
    """
    if isinstance(args, dict):
        args = argparser.argparse.Namespace(**args)

    if not isinstance(args, argparser.argparse.Namespace):
        io.critical("Argomenti non validi")

    cmd = "eksctl %s %s" % (args.action, " ".join(args.action_args))

    io.debug("Eksctl exec: %s" % str(cmd))

    if args.jq_query:
        response = commands.exec_output(cmd)
        response = text.jq(
            data=response.__str__(), query=args.jq_query, xargs=args.xargs
        )
        if args.session_save is not None:
            session.save(key=args.session_save, data={args.session_save: response})
    else:
        commands.exec(cmd)


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
