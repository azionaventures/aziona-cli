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

from aziona.core.conf import const, settings
from aziona.ingress import targets
from aziona.services.utilities import argparser, io

INGRESS = {"targets": {"module": targets, "keys": ["file", "targets"]}}


def argsinstance():
    def _targets(subparsers):
        parser_targets = subparsers.add_parser("targets", help="Aziona targets")
        parser_targets.add_argument(
            "-f",
            "--file",
            default=settings.get_aziona_template_name(),
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
    subparsers = parser.add_subparsers(help="Help for command", dest="type")

    argparser.verbosity_args(parser)

    parser.add_argument(
        "--version",
        action="version",
        version="{version}".format(version=const.getconst("VERSION")),
    )

    _targets(subparsers)

    return parser


def resolver(args: dict, keys: list):
    type = args.get("type", "undefined")

    data = {key: args[key] for key in keys}

    options = {key: args[key] for key in args.keys() if key not in keys}

    if options.get("vv") is None:
        if options.get("v") is not None and options.get("v") > options.get("verbosity"):
            options["verbosity"] = options.get("v")
        else:
            options.get("verbosity")
    else:
        options["verbosity"] = options.get("vv")

    options.pop("v")
    options.pop("vv")
    options.pop("type")

    return {"type": type, "data": data, "options": options}


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

        payload = resolver(args=args.__dict__, keys=INGRESS.get(args.type)["keys"])
        module = INGRESS.get(args.type)["module"]

        module.main(payload)

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
