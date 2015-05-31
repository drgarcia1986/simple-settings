# -*- coding: utf-8 -*-
import importlib
import os
from simple_settings.strategies.types import SettingsStrategy


def _is_python_module(file_name):
    return not file_name.endswith('.cfg')  # FIXME


def _load_python_module(settings_module):
    result = {}
    module = importlib.import_module(settings_module)
    for setting in dir(module):
        value = os.environ.get(setting, getattr(module, setting))
        result[setting] = value
    return result

strategy = SettingsStrategy(
    'python', _is_python_module, _load_python_module
)
