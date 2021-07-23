# -*- coding: utf-8 -*-

import sys

from aziona.core import argparser, commands, io


def argsinstance():
    parser = argparser.argparse.ArgumentParser()
    parser.add_argument("--cluster-name", required=True, type=str, help="Cluster name")
    parser.add_argument("--region", required=True, type=str, help="AWS region")
    parser.add_argument(
        "--kube-config", required=True, type=str, help="Kubernetes config"
    )
    parser.add_argument(
        "-p", "--profile", default=None, type=str, help="Credentials profile"
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

    cmd = "eksctl utils write-kubeconfig --cluster %s --region %s --kubeconfig %s" % (
        args.cluster_name,
        args.region,
        args.kube_config,
    )

    if args.profile is not None:
        cmd += " --profile %s" % args.profile

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
