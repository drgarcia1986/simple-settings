# -*- coding: utf-8 -*-
import importlib
import os
import sys


def _get_settings_from_cmd_line():
    for arg in sys.argv[1:]:
        if arg.startswith('--settings'):
            try:
                return arg.split('=')[1]
            except IndexError:
                return None


class _Settings(object):

    def __init__(self):
        self._dict = {}
        self._setup()

    def _setup(self):
        settings_value = _get_settings_from_cmd_line()
        if settings_value is None:
            settings_value = os.environ.get('settings')
        if settings_value is None:
            raise RuntimeError('Settings are not configured')

        self._settings_list = settings_value.split(',')
        self._load_settings_pipeline()

    def _load_settings_pipeline(self):
        for settings_module in self._settings_list:
            self._load_python_module(settings_module)

    def _load_python_module(self, settings_module):
        module = importlib.import_module(settings_module)
        for setting in dir(module):
            value = os.environ.get(setting, getattr(module, setting))
            self._dict[setting] = value

    def __getattr__(self, attr):
        return self._dict[attr]

    def as_dict(self):
        return self._dict.copy()


settings = _Settings()
