# -*- coding: utf-8 -*-
import importlib
import inspect


class SettingsLoadStrategyPython(object):
    """
    This is the strategy used to read settings from python modules.

    this strategy ignores settings starting with `_`
    """
    name = 'python'

    @classmethod
    def is_valid_file(cls, file_name):
        try:
            importlib.import_module(file_name)
            return True
        except ImportError:
            return False

    @classmethod
    def load_settings_file(cls, settings_file):
        result = {}
        module = importlib.import_module(settings_file)
        for setting in (s for s in dir(module) if not s.startswith('_')):
            setting_value = getattr(module, setting)
            if not inspect.ismodule(setting_value):
                result[setting] = setting_value
        return result
