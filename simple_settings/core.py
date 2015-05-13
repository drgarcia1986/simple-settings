# -*- coding: utf-8 -*-
import argparse
import importlib
import os


class _Settings(object):
    def __init__(self):
        self._dict = {}
        self._setup()

    def _setup(self):
        self._settings_module = self._get_settings_from_cmd_line()
        if not self._settings_module:
            self._settings_module = os.environ.get('settings')
        if not self._settings_module:
            raise RuntimeError('Settings are not configured')
        self._load_settings_module(self._settings_module)

    def _get_settings_from_cmd_line(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--settings', action='store', default='')
        return parser.parse_args().settings

    def _load_settings_module(self, settings_module):
        module = importlib.import_module(settings_module)
        for setting in dir(module):
            value = os.environ.get(setting, getattr(module, setting))
            self._dict[setting] = value

    def __getattr__(self, attr):
        return self._dict[attr]

    def as_dict(self):
        return self._dict.copy()


settings = _Settings()
