# -*- coding: utf-8 -*-
import logging.config
import os

from .constants import SPECIAL_SETTINGS_KEY


def required_settings(settings_dict):
    required_settings = (
        settings_dict[SPECIAL_SETTINGS_KEY]['REQUIRED_SETTINGS']
    )
    invalid_settings_list = [
        i for i in required_settings if i not in settings_dict
    ]
    if invalid_settings_list:
        raise ValueError(
            'The following settings are required: {}'.format(
                ', '.join(invalid_settings_list)
            )
        )


def required_not_none_settings(settings_dict):
    required_not_none_settings = (
        settings_dict[SPECIAL_SETTINGS_KEY]['REQUIRED_NOT_NONE_SETTINGS']
    )
    invalid_settings_list = [
        i for i in required_not_none_settings if settings_dict.get(i) is None
    ]
    if invalid_settings_list:
        raise ValueError(
            'The following settings are required to be not none: {}'.format(
                ', '.join(invalid_settings_list)
            )
        )


SETTINGS_TYPES = {
    'bool': bool,
    'float': float,
    'int': int,
    'str': str,
}


def required_settings_types(settings_dict):
    required_settings_types = (
        settings_dict[SPECIAL_SETTINGS_KEY]['REQUIRED_SETTINGS_TYPES']
    )
    invalid_types = [
        i for i in required_settings_types.keys() if i not in SETTINGS_TYPES
    ]
    if invalid_types:
        raise ValueError(
            'The following settings types are not valid '
            '(supported types are {}): {}'.format(
                ', '.join(SETTINGS_TYPES.keys())
            )
        )

    invalid_settings_list = []
    for key, value in settings_dict.items():
        if key in required_settings_types:
            required_type = 
            if not isinstance(value, )

    if invalid_settings_list:
        raise ValueError(
            'The following settings are required: {}'.format(
                ', '.join(invalid_settings_list)
            )
        )


def override_settings_by_env(settings_dict):
    if not settings_dict[SPECIAL_SETTINGS_KEY]['OVERRIDE_BY_ENV']:
        return
    for key, value in settings_dict.items():
        if key != SPECIAL_SETTINGS_KEY:
            settings_dict[key] = os.environ.get(key, value)


def configure_logging(settings_dict):
    if not settings_dict[SPECIAL_SETTINGS_KEY]['CONFIGURE_LOGGING']:
        return
    cfg = settings_dict.get('LOGGING')
    if cfg and isinstance(cfg, dict):
        logging.config.dictConfig(cfg)


SPECIAL_SETTINGS_MAPPING = {
    'OVERRIDE_BY_ENV': override_settings_by_env,
    'REQUIRED_SETTINGS': required_settings,
    'CONFIGURE_LOGGING': configure_logging
}


def process_special_settings(settings_dict):
    special_settings = settings_dict.get(SPECIAL_SETTINGS_KEY)
    if not special_settings:
        return

    for key, func in SPECIAL_SETTINGS_MAPPING.items():
        if key in special_settings:
            func(settings_dict)
