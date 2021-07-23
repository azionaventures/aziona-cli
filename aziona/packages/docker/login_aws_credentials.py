# -*- coding: utf-8 -*-

import sys

from aziona.core import argparser, commands, io


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument(
        "-r", "--region", required=True, default=None, type=str, help="AWS ECR REGION"
    )
    parser.add_argument(
        "-u",
        "--username",
        default="AWS",
        type=str,
        help="The registry username",
    )
    parser.add_argument(
        "-p", "--profile", default=None, type=str, help="Credentials profile"
    )
    parser.add_argument(
        "--registry", default=None, type=str, help="URL to the registry"
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

    cmd = "aws ecr get-login-password --region %s" % args.region
    if args.profile:
        cmd += " --profile %s" % args.profile

    cmd += " | docker login --username %s --password-stdin" % args.username

    if args.registry is not None:
        cmd += " %s" % args.registry

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
