# -*- coding: utf-8 -*-
"""Il modulo per la creazione di iam role su AWS
"""

import json
import sys

from botocore.exceptions import ClientError

from aziona.core import argparser, io
from aziona.core.conf import session
from aziona.packages.aws import awscli, resource_api


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument("--role-name", required=True, type=str, help="Role name")

    parser.add_argument(
        "--assumed-role-policy-document",
        required=True,
        type=str,
        help="Policy json file",
    )

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

    iam = resource_api.load(
        {
            "resource": "iam",
            "access_key": args.access_key,
            "secret_key": args.secret_key,
            "session_token": args.session_token,
            "endpointurl": args.endpoint_url,
        }
    )

    try:
        data = json.load(open(args.assumed_role_policy_document, "r"))
        response = iam.create_role(
            RoleName=args.role_name,
            AssumeRolePolicyDocument=json.dumps(data),
            Tags=[
                {"Key": "Managed By", "Value": "Aziona"},
            ],
        )
        io.info(response)
        creds = {
            "S3POLICY_ARN": response["Policy"]["Arn"],
        }
        if args.session_save:
            session.save(key=args.session_save, data=creds)
    except ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            io.warning("Policy already exists")
        else:
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
