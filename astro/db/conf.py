from pyramid.threadlocal import get_current_registry
from astro.db.exceptions import ConfigError

from sqlalchemy.orm import (
    scoped_session, sessionmaker,
)
from sqlalchemy.exc import ArgumentError
from sqlalchemy import engine_from_config


def get(key):

    settings = get_settings()

    msg = "CONFIGURATION ERROR / Requested key : " + key + \
        " not found (see pyramid .ini file)"
    if not(key in settings):
        raise ConfigError(msg)

    value = settings.get(key)

    is_empty = (len(settings.get(key)) == 0)
    if is_empty:
        raise ConfigError(msg)

    return value


def get_settings():

    settings = get_current_registry().settings
    return settings


def is_mode_debug(key):

    is_debug_mode = False

    try:
        value = get(key)
        is_debug_mode = (value == 'true')

    except ConfigError as e:
        print(e.__str__())

    return is_debug_mode


def get_engine(settings):

    engine = engine_from_config(settings, 'sqlalchemy.')

    return engine
