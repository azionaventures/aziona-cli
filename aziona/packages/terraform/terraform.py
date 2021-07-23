# -*- coding: utf-8 -*-
"""Modulo per eseguire il comando terraform
"""

import os
import sys

from aziona.core import argparser, commands, files, io
from aziona.core.conf import settings


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument(
        "--action", required=True, type=str, help="Terraform cli commands"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--module-basepath",
        default=None,
        type=str,
        help="Terraform module in default path /opt/terraform/templates. Add path to discovery your module",
    )
    group.add_argument(
        "--module-path", default=None, type=str, help="Terraform module path"
    )

    argparser.standard_args(parser)
    argparser.action_args(parser)

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

    if args.module_path:
        terraform_module_path = args.module_path
    if args.module_basepath:
        terraform_module_path = files.generate_path(
            settings.get_terraform_template_path(), args.module_basepath
        )

    if os.path.isdir(terraform_module_path) is False:
        io.critical("Terraform module not found: %s" % terraform_module_path)

    try:
        pwd = os.getcwd()
        os.chdir(terraform_module_path)
        cmd = "terraform %s %s" % (args.action, " ".join(args.action_args))
        io.debug("Terraform exec: %s" % str(cmd))
        commands.exec(cmd)
    except Exception as e:
        io.exception(e)
    finally:
        os.chdir(pwd)


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
