# -*- coding: utf-8 -*-
"""Il modulo per la creazione di record DNS sul servizio Cloudflare
"""

import sys

from aziona.core import argparser, http, io
from aziona.core.conf import settings
from aziona.packages.kubernetes import functions


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument(
        "--proxied",
        default=False,
        action="store_true",
        help="Set proxy cloudflare",
    )

    argparser.standard_args(parser)

    return parser


def scan_response(response) -> None:
    """Gestione errore creazione dns:

        - 81053 -> An A, AAAA, or CNAME record with that host already exists

    Args:
        response(requests.models.Response): risposta eseguita con il modulo requests

    Return:
        None
    """
    import requests

    try:
        io.debug(response.content.decode())
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        import json

        content = json.loads(response.content.decode())

        errors = content.get("errors", [])
        if errors == []:
            io.exception(e)

        allow_errors_code = [
            "81053"
        ]  # I codici di errore che vengono accettati e non producono errore.
        for err in errors:
            if str(err["code"]) in allow_errors_code:
                io.warning(err["message"])
            else:
                io.exception(e, err["message"])
    except Exception as e:
        io.exception(e)


def load(args) -> None:
    """Esegue la logica del modulo.

    Args:
        args(dict,argparse.Namespace,optional): argomenti richiesti dal modulo

    Returns:
        None:
    """
    if isinstance(args, dict):
        args = argparser.argparse.Namespace(**args)

    if not isinstance(args, argparser.argparse.Namespace):
        io.critical("Argomenti non validi")

    headers = {
        "Content-type": "application/json",
        "X-Auth-Email": settings.getenv("CLOUDFLARE_API_EMAIL"),
        "X-Auth-Key": settings.getenv("CLOUDFLARE_API_KEY"),
    }

    alb_ingress_domain = functions.alb_domain()

    data = {
        "type": "CNAME",
        "name": settings.getenv("APPLICATION_DOMAIN"),
        "content": alb_ingress_domain,
        "ttl": 120,
        "priority": 10,
        "proxied": args.proxied or bool(settings.getenv("CLOUDFLARE_PROXIED")),
    }

    response = http.post(
        url=settings.getenv("CLOUDFLARE_API_URL"),
        data=data,
        headers=headers,
        scan_response_func=scan_response,
    ).content.decode()

    io.info(response)


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
