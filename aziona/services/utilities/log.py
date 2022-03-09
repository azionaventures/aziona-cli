# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from aziona import settings
from aziona.services.utilities import files

try:
    LOGGER = logging.getLogger(settings.LOGGING['default']['name'])

    os.makedirs(settings.LOGGING['default']['path'], exist_ok=True)

    filename = (
        settings.LOGGING['default']['name']
        + '-'
        + str(datetime.now().strftime('%Y-%m-%d'))
        + '.log'
    )

    logging.basicConfig(
        level=logging.DEBUG,
        format=settings.LOGGING['default']['format'],
        filename=files.abspath(settings.LOGGING['default']['path'], filename),
    )
except Exception as e:
    print(str(e))
    exit(1)


def _get_logger(logger_name: str = None) -> object:
    if logger_name is None:
        return LOGGER
    return logging.getLogger(logger_name)


def info(message: str, logger_name: str = None) -> None:
    _get_logger(logger_name).info(message)


def debug(message: str, logger_name: str = None) -> None:
    _get_logger(logger_name).debug(message)


def warning(message: str, logger_name: str = None) -> None:
    _get_logger(logger_name).warning(message)


def error(message: str, logger_name: str = None) -> None:
    _get_logger(logger_name).error(message)


def critical(message: str, logger_name: str = None) -> None:
    _get_logger(logger_name).critical(message)


def exception(message: str = '', logger_name: str = None) -> None:
    _get_logger(logger_name).exception(message)
