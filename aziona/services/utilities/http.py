# -*- coding: utf-8 -*-
import requests

from aziona.core import io


def scan_response(response, args) -> None:
    try:
        io.debug(response.content.decode())
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        io.exception(e, "HTTP error occurred")
    except Exception as e:
        io.exception(e)


def post(
    url: str,
    data: dict,
    headers: dict = {},
    check_response: bool = True,
    scan_response_func=None,
    args=None,
    **kargs
):
    import json

    data = json.dumps(data)

    response = requests.post(url, headers=headers, data=data, **kargs)

    if check_response is True:
        if callable(scan_response_func):
            scan_response_func(response, args)
        else:
            scan_response(response, args)

    return response


def put(
    url: str,
    data: dict,
    headers: dict = {},
    check_response: bool = True,
    scan_response_func=None,
    args=None,
    **kargs
):
    import json

    data = json.dumps(data)

    response = requests.put(url, headers=headers, data=data, **kargs)

    if check_response is True:
        if callable(scan_response_func):
            scan_response_func(response, args)
        else:
            scan_response(response, args)

    return response


def get(
    url: str,
    headers: dict,
    check_response: bool = True,
    scan_response_func=None,
    args=None,
    **kargs
):
    response = requests.get(url, headers=headers, **kargs)

    if check_response is True:
        if callable(scan_response_func):
            scan_response_func(response, args)
        else:
            scan_response(response, args)

    return response


def delete(
    url: str,
    headers: dict,
    check_response: bool = True,
    scan_response_func=None,
    args=None,
    **kargs
):
    response = requests.delete(url, headers=headers, **kargs)

    if check_response is True:
        if callable(scan_response_func):
            scan_response_func(response, args)
        else:
            scan_response(response, args)

    return response
