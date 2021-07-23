# -*- coding: utf-8 -*-
"""Il modulo assumere un ruolo specifico, restituisce la sessione
"""
import sys

from aziona.core import argparser, io
from aziona.packages.aws import awscli, resource_api


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    argparser.standard_args(parser)

    awscli.standard_args(parser)

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

    # create an STS client object that represents a live connection to the
    # STS service
    sts = resource_api.load(
        {
            "resource": "sts",
            "access_key": args.access_key,
            "secret_key": args.secret_key,
            "session_token": args.session_token,
            "endpointurl": args.endpoint_url,
        }
    )

    identity = sts.get_caller_identity()
    io.info(
        "STS ACCOUNT IDENTITY\n- Account: %s\n- Arn: %s"
        % (identity["Account"], identity["Arn"])
    )


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
