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

from aziona.cli.parser import parser
from aziona.core import argparser, io, log
from aziona.core.conf import const, settings


def argsinstance():
    parser = argparser.argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version="{version}".format(version=const.getconst("VERSION")),
    )

    parser.add_argument(
        "-f",
        "--file",
        default=settings.get_aziona_template_name(),
        type=str,
        help="Nome del template o del path(compreso del nome).",
    )

    parser.add_argument(
        "targets",
        metavar="targets",
        type=str,
        nargs="+",
        help="Target che verrano eseguiti a partire dal template indicato. Verrano eseguiti in sequenza.",
    )

    argparser.verbosity_args(parser)

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

        log.info("------", "start")

        # TODO fix temporaneo per supportare .devops.yml
        import os

        filename = args.file
        if os.path.isfile(".devops.yml") is True:
            filename = ".devops.yml"
        #

        parsed = parser.Parser(filename=filename)
        io.info("Esecuzione file: %s" % filename)
        parsed.main(args.targets)
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
