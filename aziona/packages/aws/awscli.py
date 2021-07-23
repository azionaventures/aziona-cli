# -*- coding: utf-8 -*-
"""Il modulo per la cancellazione di record DNS sul servizio route53 di AWS
"""
import sys

import botocore
from awscli import clidriver

from aziona.core import argparser, io, text
from aziona.core.conf import errors, session

REGION = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-central-1",
    "ap-east-1",
    "me-south-1",
    "us-gov-west-1",
    "us-gov-east-1",
    "us-iso-east-1",
    "us-isob-east-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-south-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "eu-north-1",
    "sa-east-1",
    "ca-central-1",
    "cn-north-1",
    "af-south-1",
    "eu-south-1",
]


def standard_args(parser):
    if not isinstance(parser, argparser.argparse.ArgumentParser):
        raise errors.ParamTypeError(param="parser", type="argparse.ArgumentParser")

    parser.add_argument("--resource", type=str, help="Access key,")
    parser.add_argument(
        "--access-key",
        default=None,
        type=str,
        help="Access key se non specificato usa AWS_ACCESS_KEY_ID",
    )
    parser.add_argument(
        "--secret-key",
        default=None,
        type=str,
        help="Secret key, se non specificato usa AWS_SECRET_ACCESS_KEY",
    )
    parser.add_argument(
        "--region-name",
        default=None,
        type=str,
        choices=REGION,
        help="Nome regione, se non specificato usa AWS_DEFAULT_REGION",
    )
    parser.add_argument(
        "--session-token",
        default=None,
        type=str,
        help="Token di sessione, se non specificato usa AWS_SESSION_TOKEN",
    )
    parser.add_argument(
        "--profile-name",
        default=None,
        type=str,
        help="Profilo aws, se non specificato usa AWS_PROFILE",
    )
    parser.add_argument(
        "--endpoint-url",
        default=None,
        type=str,
        help="AWS endpointurl",
    )

    parser.add_argument("--account-id", default=None, type=str, help="AWS Account id")

    return parser


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument("--action", required=True, type=str, help="Aws cli commands")

    standard_args(parser)
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
        args = argparser.namespace_from_dict(argsinstance()._actions, args)

    if not isinstance(args, argparser.argparse.Namespace):
        raise errors.ParamTypeError(param="args", type="argparse.Namespace")

    # Init awscli
    session_botocore = botocore.session.Session(profile=args.profile_name)
    aws = clidriver.CLIDriver(session_botocore)
    # @TODO FIX: opzioni aws non ricosciute ad es. aws --endpoint-url .. [AZIONE] [ARGS]
    # Esempio funzionante: ['s3','list-buckets']
    with io.Capturing() as response:
        aws.main([args.action, *args.action_args])

    if args.jq_query:
        response = text.jq(
            data=response.__str__(), query=args.jq_query, xargs=args.xargs
        )

    if args.session_save is not None:
        session.save(key=args.session_save, data={args.session_save: response})


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
