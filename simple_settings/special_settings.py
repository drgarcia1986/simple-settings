import json
import logging.config
import os
from collections import OrderedDict
from distutils.util import strtobool

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
            'The following settings are required '
            'to have a value that is not none: {}'.format(
                ', '.join(invalid_settings_list)
            )
        )


SETTINGS_TYPES = {
    'bool': (bool, lambda x: bool(strtobool(x))),
    'float': (float, float),
    'int': (int, int),
    'str': (str, str),
    'json.loads': ((dict, list), json.loads)
}


def required_settings_types(settings_dict):
    required_settings_types = (
        settings_dict[SPECIAL_SETTINGS_KEY]['REQUIRED_SETTINGS_TYPES']
    )
    unsupported_types = [
        key for key, value in required_settings_types.items()
        if value not in SETTINGS_TYPES
    ]
    if unsupported_types:
        raise ValueError(
            'The following settings types are not unsupported '
            '(supported types are {}): {}'.format(
                ', '.join(SETTINGS_TYPES.keys()), ', '.join(unsupported_types)
            )
        )

    invalid_settings_list = []
    for key, value in settings_dict.items():
        if key in required_settings_types:
            settings_type = required_settings_types[key]
            required_type, parser = SETTINGS_TYPES[settings_type]
            # None values are allowed as they can be of any type
            if value is not None and not isinstance(value, required_type):
                try:
                    # only attempt conversion from string
                    if not isinstance(value, str):
                        raise ValueError
                    settings_dict[key] = parser(value)
                except ValueError:
                    invalid_settings_list.append((key, settings_type))

    if invalid_settings_list:
        raise ValueError(
            'The following settings are required '
            'to have a value of a specific type: {}'.format(
                ', '.join(
                    '{} ({})'.format(key, required_type)
                    for key, required_type in invalid_settings_list
                )
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


SPECIAL_SETTINGS_MAPPING = OrderedDict((
    ('OVERRIDE_BY_ENV', override_settings_by_env),
    ('REQUIRED_SETTINGS', required_settings),
    ('REQUIRED_NOT_NONE_SETTINGS', required_not_none_settings),
    ('REQUIRED_SETTINGS_TYPES', required_settings_types),
    ('CONFIGURE_LOGGING', configure_logging),
))


def process_special_settings(settings_dict):
    special_settings = settings_dict.get(SPECIAL_SETTINGS_KEY)
    if not special_settings:
        return

    for key, func in SPECIAL_SETTINGS_MAPPING.items():
        if key in special_settings:
            func(settings_dict)
