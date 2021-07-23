# -*- coding: utf-8 -*-
"""Il modulo per la creazione di iam policy su AWS
"""

import argparse
import sys

from aziona.core import argparser, commands, io


def argsinstance():
    parser = argparse.ArgumentParser()

    parser.add_argument("--action", required=True, type=str, help="Action")

    parser.add_argument("--cluster", required=True, type=str, help="EKS Cluster")

    parser.add_argument("--profile", type=str, help="EKS profile")

    parser.add_argument("--region", required=True, type=str, help="EKS Cluster Region")

    parser.add_argument("--name", required=True, type=str, help="Service account name")

    parser.add_argument(
        "--namespace", default="default", type=str, help="EKS default namespace"
    )

    parser.add_argument(
        "--attach-policy-arn",
        required=False,
        default=None,
        type=str,
        help="IAM Policy arn to be attached",
    )

    parser.add_argument(
        "--override-existing-serviceaccounts",
        default=False,
        action="store_true",
        help="Override existing service accounts",
    )

    parser.add_argument(
        "--approve", default=False, action="store_true", help="auto approve"
    )

    argparser.standard_args(parser)

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

    if args.action == "create":
        cmd = "eksctl create iamserviceaccount"
        cmd += " --cluster %s" % args.cluster
        cmd += " --region %s" % args.region
        if args.profile:
            cmd += " --profile %s" % args.profile
        cmd += " --name %s" % args.name
        cmd += " --namespace %s" % args.namespace
        cmd += " --attach-policy-arn %s" % args.attach_policy_arn

        if args.override_existing_serviceaccounts:
            cmd += " --override-existing-serviceaccounts"

        if args.approve:
            cmd += " --approve"

        commands.exec(cmd)

    elif args.action == "delete":
        cmd = "eksctl delete iamserviceaccount"
        cmd += " --cluster %s" % args.cluster
        cmd += " --region %s" % args.region
        if args.profile:
            cmd += " --profile %s" % args.profile
        cmd += " --name %s" % args.name
        cmd += " --namespace %s" % args.namespace

        commands.exec(cmd)


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
