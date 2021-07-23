# -*- coding: utf-8 -*-
import os
import pickle

from aziona.core import io
from aziona.core.conf import errors, settings


def _obj_session_save(session: dict, session_filepath: str = None):
    if not isinstance(session, dict):
        raise errors.ParamTypeError(param="session", type="dict")
    pickle.dump(
        session,
        open(settings.get_session_path(session_filepath=session_filepath), "wb"),
    )


def _obj_session_get(session_filepath: str = None) -> dict:
    path = settings.get_session_path(session_filepath=session_filepath)

    if os.path.isfile(path) is False:
        io.warning("Session obj not found: %s" % session_filepath)
        return {}

    return pickle.load(open(path, "rb"))


def _obj_session_del(session_filepath: str = None):
    path = settings.get_session_path(session_filepath=session_filepath)
    if os.path.isfile(path) is True:
        os.remove(path)


def get(key: str = None, session_filepath: str = None) -> dict:
    data = _obj_session_get(session_filepath=session_filepath)

    if isinstance(key, str):
        return {key: data.get(key, {})}

    return data


def load(key: str = None, session_filepath: str = None) -> None:
    session = get(key=key, session_filepath=session_filepath)

    for name, data in session.items():
        settings.setenv_from_dict(overwrite=True, **data)
        io.info("Session %s loaded success" % name)


def clean(key: str = None, session_filepath: str = None):
    if key is None:
        _obj_session_del(session_filepath)
        return

    session = get(session_filepath=session_filepath)

    session.pop(key)

    _obj_session_save(session, session_filepath)


def save(key: str, data: dict, session_filepath: str = None) -> dict:
    if not isinstance(key, str):
        raise errors.ParamTypeError(param="key", type="str")

    if not isinstance(data, dict):
        raise errors.ParamTypeError(param="data", type="dict")

    session = get(session_filepath=session_filepath)

    session[key] = {key: str(item) for key, item in data.items()}

    _obj_session_save(session, session_filepath)

    return session
