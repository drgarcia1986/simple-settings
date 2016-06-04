# -*- coding: utf-8 -*-
import importlib

from simple_settings.constants import (
    DYNAMIC_SETTINGS_KEY,
    SPECIAL_SETTINGS_KEY
)

DYNAMIC_SETTINGS_MAPPING = {
    'consul': 'simple_settings.dynamic_settings.consul_reader',
    'database': 'simple_settings.dynamic_settings.database_reader',
    'redis': 'simple_settings.dynamic_settings.redis_reader',
}


def get_dynamic_reader(settings_dict):
    dynamic_settings_conf = (
        settings_dict.get(SPECIAL_SETTINGS_KEY, {}).get(DYNAMIC_SETTINGS_KEY)
    )
    if not dynamic_settings_conf:
        return

    reader_backend = dynamic_settings_conf['backend']
    if reader_backend in DYNAMIC_SETTINGS_MAPPING:
        reader_backend = DYNAMIC_SETTINGS_MAPPING[reader_backend]

    reader_module = importlib.import_module(reader_backend)
    reader = reader_module.Reader(dynamic_settings_conf)

    return reader
