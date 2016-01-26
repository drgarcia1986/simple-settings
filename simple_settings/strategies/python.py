# -*- coding: utf-8 -*-
import importlib
import inspect


class SettingsLoadStrategyPython(object):

    name = 'python'

    def is_valid_file(self, file_name):
        try:
            importlib.import_module(file_name)
            return True
        except ImportError:
            return False

    def load_settings_file(self, settings_file):
        result = {}
        module = importlib.import_module(settings_file)
        for setting in (s for s in dir(module) if not s.startswith('_')):
            setting_value = getattr(module, setting)
            if not inspect.ismodule(setting_value):
                result[setting] = setting_value
        return result
