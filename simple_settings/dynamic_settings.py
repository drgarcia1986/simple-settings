# -*- coding: utf-8 -*-
import os


DYNAMIC_SETTINGS_KEY = 'DYNAMIC_SETTINGS'


def get_by_env(setting):
    return os.environ.get(setting)


DYNAMIC_SETTINGS_MAPPING = {
    'ENV': get_by_env
}


def process_dynamic_settings(settings_dict, setting):
    dynamic_settings_strategies = settings_dict.get(DYNAMIC_SETTINGS_KEY)
    if not dynamic_settings_strategies:
        return

    result = None
    for key, func in DYNAMIC_SETTINGS_MAPPING.items():
        if key in dynamic_settings_strategies:
            result = func(setting) or result

    return result
