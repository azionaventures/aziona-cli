# -*- coding: utf-8 -*-
"""Modulo per eseguire il comando terraform
"""

import os
import sys

from aziona.core import argparser, commands, files, gitmanager, io
from aziona.core.conf import settings


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument(
        "--action", required=True, type=str, help="Terraform cli commands"
    )

    parser.add_argument(
        "--path-to-module", type=str, help="Navigate to a specific path in the module"
    )

    parser.add_argument("--tag", type=str, help="Git tag to clone")

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
    group.add_argument(
        "--module-git", default=None, type=str, help="Terraform git module"
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
            settings.get_terraform_modules_path(), args.module_basepath
        )
    if args.module_git:
        terraform_modules_path = settings.getenv(
            key="AZIONA_MODULES_PATH"
        )  # all modules path
        os.makedirs(terraform_modules_path, exist_ok=True)
        project_name = args.module_git.split("/")[-1][
            :-4
        ]  # git@domain:/path/to/XXXXXXXX.git
        terraform_module_path = (
            terraform_modules_path + "/" + project_name
        )  # current module path
        gitmanager.clone(
            project_name, terraform_modules_path, args.module_git, args.tag
        )

    if args.path_to_module:
        terraform_module_path = terraform_module_path + "/" + args.path_to_module

    if os.path.isdir(terraform_module_path) is False:
        io.critical("Aziona module not found: %s" % terraform_module_path)

    try:
        pwd = os.getcwd()
        os.chdir(terraform_module_path)
        cmd = "aziona %s %s" % (args.action, " ".join(args.action_args))
        io.debug("Aziona exec: %s" % str(cmd))
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
