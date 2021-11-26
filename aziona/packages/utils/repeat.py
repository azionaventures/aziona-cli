# -*- coding: utf-8 -*-
"""Modulo per eseguire comandi shell ricorsivi
"""
import sys
from time import sleep

from aziona.core import argparser, commands, io


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument(
        "-a", "--action", required=True, type=str, help="Schell Command"
    )
    parser.add_argument("-r", "--repeat", default=1, type=int, help="Repeat command")
    parser.add_argument(
        "-s", "--sleep", default=0.0, type=float, help="Sleep time between executions"
    )

    argparser.standard_args(parser)
    argparser.action_args(parser)

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

    if args.repeat < 0:
        io.warning("Repeat count invalid. Autoset to default: 0")
        args.repeat = 1

    for counter in range(args.repeat):
        io.debug(f"Repeat counter: {counter+1}")
        commands.exec_check(args.action + " " + " ".join(args.action_args))
        sleep(args.sleep)


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
