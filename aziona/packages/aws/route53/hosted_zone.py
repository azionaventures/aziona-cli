# -*- coding: utf-8 -*-
"""Il modulo assumere un ruolo specifico, restituisce la sessione
"""


import sys

from aziona.core import argparser, io
from aziona.core.conf import session
from aziona.packages.aws import awscli, resource_session

TYPE = ["CNAME", "A"]


def argsinstance():
    parser = argparser.argparse.ArgumentParser(description="Create DNS records on R53")

    parser.add_argument("--name", required=True, type=str)
    parser.add_argument("--caller-ref", required=True, type=str)
    parser.add_argument("--vpc-region", choices=awscli.REGION, type=str)
    parser.add_argument("--vpc-id", type=str)
    parser.add_argument("--vpc-comment", default="", type=str)
    parser.add_argument("--vpc-private", default=False, action="store_true")

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

    route53 = resource_session.load(
        {
            "resource": "route53",
            "access_key": args.access_key,
            "secret_key": args.secret_key,
            "session_token": args.session_token,
            "endpointurl": args.endpoint_url,
        }
    )

    kargs = {
        "Name": args.name,
        "CallerReference": args.caller_ref,
        "HostedZoneConfig": {
            "Comment": args.vpc_comment,
            "PrivateZone": args.vpc_private,
        },
    }

    if args.vpc_private is True:
        kargs["VPC"] = {"VPCRegion": args.vpc_region, "VPCId": args.vpc_id}

    response = route53.create_hosted_zone(**kargs)
    io.debug(response)

    if args.session_save is not None:
        session.save(
            key=args.session_save, data={"HOSTED_ZONE": response["HostedZone"]["Id"]}
        )

    return response


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
