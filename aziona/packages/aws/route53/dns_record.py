# -*- coding: utf-8 -*-
"""Il modulo assumere un ruolo specifico, restituisce la sessione
"""
import sys

from aziona.core import argparser, io
from aziona.core.conf import settings
from aziona.packages.aws import awscli, resource_session
from aziona.packages.kubernetes import functions

TYPE = ["CNAME", "A"]

ACTION = ["CREATE", "DELETE", "UPSERT"]


def argsinstance():
    parser = argparser.argparse.ArgumentParser(description="Create DNS records on R53")

    parser.add_argument("--hosted-zone-id", default=None, type=str)
    parser.add_argument("--name", required=True, type=str)
    parser.add_argument("--type", choices=TYPE, required=True, type=str)
    parser.add_argument("--action", choices=ACTION, required=True)
    parser.add_argument("--ttl", default=300, type=int)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--value", type=str)
    group.add_argument("--value-alb-domain", default=False, action="store_true")

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

    value = functions.alb_domain() if args.value_alb_domain is True else args.value

    response = route53.change_resource_record_sets(
        HostedZoneId=args.hosted_zone_id or settings.getenv("HOSTED_ZONE"),
        ChangeBatch={
            "Comment": "add %s -> %s" % (args.name, value),
            "Changes": [
                {
                    "Action": args.action,
                    "ResourceRecordSet": {
                        "Name": args.name,
                        "Type": args.type,
                        "TTL": args.ttl,
                        "ResourceRecords": [{"Value": value}],
                    },
                }
            ],
        },
    )

    io.debug(response)


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
