# -*- coding: utf-8 -*-
"""Il modulo log.py configura il logger ed espone le funzioni per scrivere nel file log

Attributes:

- LOGGER (logging): object

"""
import logging
import os

from aziona.core.conf import settings

try:
    LOGGER = logging.getLogger(settings.get_logging_name() + ".root")
    os.makedirs(settings.get_logging_basepath(), exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format=settings.get_logging_format(),
        filename=settings.get_logging_filepath(),
    )
except Exception as e:
    print(str(e))
    exit(1)


def _get_logger(logger_name: str = None) -> object:
    if logger_name is None:
        return LOGGER
    return logging.getLogger(logger_name)


def info(message: str, logger_name: str = None) -> None:
    """Log info

    Args:
        message (str): Messaggio da scrivere nel log

    Returns:
        None

    Raises:
        None
    """
    _get_logger(logger_name).info(message)


def debug(message: str, logger_name: str = None) -> None:
    """Log debug

    Args:
        message (str): Messaggio da scrivere nel log

    Returns:
        None

    Raises:
        None
    """
    _get_logger(logger_name).debug(message)


def warning(message: str, logger_name: str = None) -> None:
    """Log warning

    Args:
        message (str): Messaggio da scrivere nel log

    Returns:
        None

    Raises:
        None
    """
    _get_logger(logger_name).warning(message)


def error(message: str, logger_name: str = None) -> None:
    """Log error

    Args:
        message (str): Messaggio da scrivere nel log

    Returns:
        None

    Raises:
        None
    """
    _get_logger(logger_name).error(message)


def critical(message: str, logger_name: str = None) -> None:
    """Log critical

    Args:
        message (str): Messaggio da scrivere nel log

    Returns:
        None

    Raises:
        None
    """
    _get_logger(logger_name).critical(message)


def exception(message: str = "", logger_name: str = None) -> None:
    """Log exception

    Args:
        message (str): Messaggio da scrivere nel log

    Returns:
        None

    Raises:
        None
    """
    _get_logger(logger_name).exception(message)
