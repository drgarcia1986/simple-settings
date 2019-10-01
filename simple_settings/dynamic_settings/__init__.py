# -*- coding: utf-8 -*-
import importlib

from simple_settings.constants import (
    DYNAMIC_SETTINGS_KEY,
    SPECIAL_SETTINGS_KEY
)

DYNAMIC_SETTINGS_MAPPING = {
    'consul': 'simple_settings.dynamic_settings.consul_reader.Reader',
    'database': 'simple_settings.dynamic_settings.database_reader.Reader',
    'memcached': 'simple_settings.dynamic_settings.memcached_reader.Reader',
    'redis': 'simple_settings.dynamic_settings.redis_reader.Reader',
    's3': 'simple_settings.dynamic_settings.s3_reader.Reader'
}


class InvalidDynamicSettingsReaderPath(RuntimeError):

    def __init__(self, path):
        super(InvalidDynamicSettingsReaderPath, self).__init__(self)
        self.path = path

    def __str__(self):
        return 'The path of dynamic settings reader [{}] is invalid'.format(
            self.path
        )


def get_dynamic_reader(settings_dict):
    dynamic_settings_conf = (
        settings_dict.get(SPECIAL_SETTINGS_KEY, {}).get(DYNAMIC_SETTINGS_KEY)
    )
    if not dynamic_settings_conf:
        return

    reader_backend = dynamic_settings_conf['backend']
    if reader_backend in DYNAMIC_SETTINGS_MAPPING:
        reader_backend = DYNAMIC_SETTINGS_MAPPING[reader_backend]

    reader_class = get_dynamic_reader_class(reader_backend)
    return reader_class(dynamic_settings_conf)


def get_dynamic_reader_class(reader_backend_path):
    try:
        module_path, class_name = reader_backend_path.rsplit('.', 1)
        reader_module = importlib.import_module(module_path)
        return getattr(reader_module, class_name)
    except (ValueError, ImportError, AttributeError):
        raise InvalidDynamicSettingsReaderPath(reader_backend_path)
