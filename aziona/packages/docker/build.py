# -*- coding: utf-8 -*-

import sys

from aziona.core import argparser, commands, io


def argsinstance():
    parser = argparser.argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        default=None,
        type=str,
        help="Path to the directory containing the Dockerfile",
    )
    parser.add_argument(
        "-d",
        "--dockerfile",
        default=None,
        type=str,
        help="path within the build context to the Dockerfile",
    )
    parser.add_argument(
        "--target",
        default=None,
        type=str,
        help="Name of the build-stage to build in a multi-stage Dockerfile",
    )
    parser.add_argument(
        "-t", "--tag", default=None, type=str, help="A tag to add to the final image"
    )
    parser.add_argument(
        "--tag-secondary",
        default=None,
        type=str,
        nargs="+",
        help="A tag to add to the final image",
    )

    parser.add_argument(
        "--build-args",
        action=argparser.StoreActionArgsParser,
        default=[],
        nargs="+",
        type=str,
        help="Build args",
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

    cmd = "docker build"

    if args.tag is not None:
        cmd += " -t %s" % args.tag

    if args.dockerfile is not None:
        cmd += " -f %s" % args.dockerfile

    if args.target is not None:
        cmd += " --target %s" % args.target

    if args.path is not None:
        cmd += " %s" % args.path

    if args.build_args is not None:
        cmd += " %s" % " ".join(["--build-arg %s" % arg for arg in args.build_args])

    commands.exec(cmd)

    if args.tag and args.tag_secondary:
        for tag in args.tag_secondary:
            commands.exec("docker tag %s %s" % (args.tag, tag))


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
