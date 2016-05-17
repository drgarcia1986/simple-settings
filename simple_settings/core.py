# -*- coding: utf-8 -*-
from copy import deepcopy
import os
import sys

from .special_settings import process_special_settings
from .strategies import strategies


class LazySettings(object):
    """
    LazySettings is the main class of simple-settings

    To use just create a instance and access the attributes
    of your settings files.

    Read the docs for more informations:
        http://simple-settings.readthedocs.org/en/latest/
    """
    ENVIRON_KEYS = ('settings', 'SIMPLE_SETTINGS')
    COMMAND_LINE_ARGS = ('--settings', '--simple-settings')

    def __init__(self, *settings_list):
        self._settings_list = list(settings_list)
        self._initialized = False
        self._dict = {}

    def _get_settings_from_cmd_line(self):
        for arg in sys.argv[1:]:
            for lib_arg in self.COMMAND_LINE_ARGS:
                if arg.startswith(lib_arg):
                    try:
                        return arg.split('=')[1]
                    except IndexError:
                        return
        return

    def _get_settings_from_environ(self):
        for key in self.ENVIRON_KEYS:
            if key in os.environ:
                return os.environ[key]
        return

    def _get_settings_value(self):
        return (
            self._get_settings_from_cmd_line() or
            self._get_settings_from_environ()
        )

    def setup(self):
        if self._initialized:
            return

        if not self._settings_list:
            settings_value = self._get_settings_value()
            if not settings_value:
                raise RuntimeError('Settings are not configured')
            self._settings_list = settings_value.split(',')

        self._load_settings_pipeline()
        process_special_settings(self._dict)
        self._initialized = True

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
        self.setup()
        try:
            return self._dict[attr]
        except KeyError:
            raise AttributeError('You do not set {} setting'.format(attr))

    def configure(self, **settings):
        self._dict.update(settings)

    def as_dict(self):
        self.setup()
        return deepcopy(self._dict)


settings = LazySettings()
