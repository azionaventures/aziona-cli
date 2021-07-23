# -*- coding: utf-8 -*-
"""Il modulo assumere un ruolo specifico, restituisce la sessione
"""


import sys

from aziona.core import argparser, io
from aziona.core.conf import session
from aziona.packages.aws import awscli, resource_api


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument(
        "--role-arn", required=True, type=str, help="Role arn da assumere"
    )

    parser.add_argument(
        "--role-session-name", required=True, type=str, help="Nome della sessione"
    )

    parser.add_argument(
        "--role-session-duration", default=3600, type=int, help="Durata della sessione"
    )

    argparser.standard_args(parser)

    awscli.standard_args(parser)

    return parser


def load(args) -> dict:
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

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    role = sts.assume_role(
        RoleArn=args.role_arn,
        RoleSessionName=args.role_session_name,
        DurationSeconds=args.role_session_duration,
    )

    creds = {
        "AWS_ACCESS_KEY_ID": role["Credentials"]["AccessKeyId"],
        "AWS_SECRET_ACCESS_KEY": role["Credentials"]["SecretAccessKey"],
        "AWS_SESSION_TOKEN": role["Credentials"]["SessionToken"],
    }

    if args.session_save:
        session.save(key=args.session_save, data=creds)

    # Use the temporary credentials that AssumeRole for session resource
    return creds


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
