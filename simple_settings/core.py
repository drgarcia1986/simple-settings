# -*- coding: utf-8 -*-
import os
import sys

from .strategies import strategies


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
        for settings_file in self._settings_list:
            strategy = self._get_strategy_by_file(settings_file)
            if strategy is None:
                raise RuntimeError(
                    'Invalid setting file [{}]'.format(settings_file)
                )
            settings = strategy.load_settings_file(settings_file)
            self._dict.update(settings)

    def _get_strategy_by_file(self, settings_file):
        for strategy in strategies:
            if strategy.is_valid_file(settings_file):
                return strategy

    def __getattr__(self, attr):
        return self._dict[attr]

    def as_dict(self):
        return self._dict.copy()


settings = _Settings()
