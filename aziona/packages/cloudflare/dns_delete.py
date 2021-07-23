# -*- coding: utf-8 -*-
"""Il modulo per la cancellazione di record DNS sul servizio Cloudflare
"""
import sys

from aziona.core import argparser, commands, http, io
from aziona.core.conf import settings


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

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

    headers = {
        "Content-type": "application/json",
        "X-Auth-Email": settings.getenv("CLOUDFLARE_API_EMAIL"),
        "X-Auth-Key": settings.getenv("CLOUDFLARE_API_KEY"),
    }

    response = http.get(
        url=settings.getenv("CLOUDFLARE_API_URL"), headers=headers
    ).content.decode()

    io.info(response)

    cmd = "echo '%s' | jq -r '.result[] | select(.name == \"%s\") | .id'" % (
        response,
        settings.getenv("APPLICATION_DOMAIN"),
    )

    id_record = commands.exec_output(cmd)

    io.info(id_record)

    if id_record:
        response = http.delete(
            url=settings.getenv("CLOUDFLARE_API_URL") + "/%s" % id_record,
            headers=headers,
        )


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
