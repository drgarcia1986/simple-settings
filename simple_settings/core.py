# -*- coding: utf-8 -*-
import copy
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

    SPECIAL_SETTINGS_KEY = 'SIMPLE_SETTINGS'

    def __init__(self):
        self._dict = {}
        self._settings_list = []
        self._setup()

    def _setup(self):
        settings_value = _get_settings_from_cmd_line()
        if not settings_value:
            settings_value = os.environ.get('settings')
        if not settings_value:
            raise RuntimeError('Settings are not configured')

        self._settings_list = settings_value.split(',')
        self._load_settings_pipeline()
        self._process_special_settings()

    def _override_settings_by_env(self):
        for key, value in self._dict.items():
            self._dict[key] = os.environ.get(key, value)

    def _process_special_settings(self):
        if self.SPECIAL_SETTINGS_KEY not in self._dict:
            return

        if self._dict[self.SPECIAL_SETTINGS_KEY].get('OVERRIDE_BY_ENV'):
            self._override_settings_by_env()

    def _load_settings_pipeline(self):
        for settings_file in self._settings_list:
            strategy = self._get_strategy_by_file(settings_file)
            if not strategy:
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
        return copy.deepcopy(self._dict)


settings = _Settings()
