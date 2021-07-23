# -*- coding: utf-8 -*-
"""Il modulo per la cancellazione di record DNS sul servizio route53 di AWS
"""


import sys

import boto3

from aziona.core import argparser, io
from aziona.packages.aws import awscli


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

    session = boto3.session.Session(
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key,
        aws_session_token=args.session_token,
        region_name=args.region_name,
        profile_name=args.profile_name,
    )

    if args.resource is None:
        return session

    return session.client(
        service_name=args.resource,
        endpoint_url=args.endpoint_url,
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
