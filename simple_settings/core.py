# -*- coding: utf-8 -*-
from copy import deepcopy
import os
import sys

from .strategies import strategies


class LazySettings(object):
    """
    LazySettings is the main class of simple-settings

    To use just create a instance and access the attributes
    of your settings files.

    Read the docs for more informations:
        http://simple-settings.readthedocs.org/en/latest/
    """
    SPECIAL_SETTINGS_KEY = 'SIMPLE_SETTINGS'

    def __init__(self):
        self._dict = {}
        self._settings_list = []
        self._initialized = False

    def _get_settings_from_cmd_line(self):
        for arg in sys.argv[1:]:
            if (
                arg.startswith('--settings')
                or arg.startswith('--simple-settings')
            ):
                try:
                    return arg.split('=')[1]
                except IndexError:
                    return

    def _setup(self):
        if self._initialized:
            return

        settings_value = self._get_settings_from_cmd_line()
        if not settings_value:
            settings_value = (
                os.environ.get('settings')
                or os.environ.get('SIMPLE_SETTINGS')
            )
        if not settings_value:
            raise RuntimeError('Settings are not configured')

        self._settings_list = settings_value.split(',')
        self._load_settings_pipeline()
        self._process_special_settings()

        self._initialized = True

    def _override_settings_by_env(self):
        for key, value in self._dict.items():
            self._dict[key] = os.environ.get(key, value)

    def _required_settings(self):
        required_settings = (
            self._dict[self.SPECIAL_SETTINGS_KEY]['REQUIRED_SETTINGS']
        )
        invalid_settings_list = [
            i for i in required_settings if i not in self._dict
        ]
        if invalid_settings_list:
            raise ValueError(
                'The following settings are required: {}'.format(
                    ', '.join(invalid_settings_list)
                )
            )

    def _process_special_settings(self):
        special_settings = self._dict.get(self.SPECIAL_SETTINGS_KEY)
        if not special_settings:
            return

        if special_settings.get('OVERRIDE_BY_ENV'):
            self._override_settings_by_env()

        if special_settings.get('REQUIRED_SETTINGS'):
            self._required_settings()

    def _load_settings_pipeline(self):
        for settings_file in self._settings_list:
            strategy = self._get_strategy_by_file(settings_file)
            settings = strategy.load_settings_file(settings_file)
            self._dict.update(settings)

    def _get_strategy_by_file(self, settings_file):
        for strategy in strategies:
            if strategy.is_valid_file(settings_file):
                return strategy
        raise RuntimeError('Invalid settings file [{}]'.format(settings_file))

    def __getattr__(self, attr):
        self._setup()
        try:
            return self._dict[attr]
        except KeyError:
            raise AttributeError('You do not set {} setting'.format(attr))

    def as_dict(self):
        self._setup()
        return deepcopy(self._dict)


settings = LazySettings()
