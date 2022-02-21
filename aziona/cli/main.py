# -*- coding: utf-8 -*-
"""Il modulo è l'entrypoint per il devosps-runner. \
Ha il compito di processare il file yml contentente il template con le azioni da eseguire. \
Ogni azione viene eseguita come sotto processo e inizializzato con un env costruito a partire
da quello host più eventuali varibili definite nel template. \
L'esecuzione può essere di uno o più target in modo sequenziale (in ordine di inserimento da command line), se
l'esecuzione va in errore allora il processo master si interromperà non eseguendo i successivi target indicati,
è possibile inibire l'interruzione per uno o più target con apposite regole nel template.
"""


import sys

from aziona import settings
from aziona.ingress import route
from aziona.services.utilities import argparser, io

__OPTIONS__ARGS__ = ("type", "v", "vv", "verbosity")


def argsinstance():
    def _targets(subparsers):
        parser_targets = subparsers.add_parser("targets", help="Aziona targets")
        parser_targets.add_argument(
            "-f",
            "--filename",
            default=settings.TEMPLATE_FILE_NAME,
            type=str,
            help="Nome del template o del path(compreso del nome).",
        )
        parser_targets.add_argument(
            "targets",
            metavar="targets",
            type=str,
            nargs="+",
            help="Target che verrano eseguiti a partire dal template indicato. Verrano eseguiti in sequenza.",
        )

    parser = argparser.argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version="{version}".format(version=settings.VERSION),
    )
    subparsers = parser.add_subparsers(help="Help for command", dest="type")

    argparser.verbosity_args(parser)

    _targets(subparsers)

    return parser


def load(args) -> None:
    """Esegue la logica del modulo.

    Args:
        args(dict,argparse.Namespace,optional): argomenti richiesti dal modulo

    Returns:
        None:
    """
    try:
        if isinstance(args, dict):
            args = argparser.namespace_from_dict(argsinstance()._actions, args)

        if not isinstance(args, argparser.argparse.Namespace):
            io.critical("Argomenti non validi")

        r = route.get(
            args.type,
            data={
                k: v for k, v in vars(args).items() if k not in __OPTIONS__ARGS__
            },  # Excludes arguments option cli
        )

        r.run()
    except Exception as e:
        io.exception(e)


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
