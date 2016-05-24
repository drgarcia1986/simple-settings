# -*- coding: utf-8 -*-
import os

from .constants import DYNAMIC_SETTINGS_KEY, SPECIAL_SETTINGS_KEY


DYNAMIC_SETTINGS_MAPPING = {
    'ENV': lambda setting: os.environ.get(setting)
}


def process_dynamic_settings(settings_dict, setting):
    dynamic_settings_strategies = (
        settings_dict.get(SPECIAL_SETTINGS_KEY, {}).get(DYNAMIC_SETTINGS_KEY)
    )
    if not dynamic_settings_strategies:
        return

    result = None
    for key, func in DYNAMIC_SETTINGS_MAPPING.items():
        if key in dynamic_settings_strategies:
            result = func(setting) or result

    return result
