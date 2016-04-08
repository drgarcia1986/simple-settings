# -*- coding: utf-8 -*-
from functools import wraps

from .core import settings


class settings_stub(object):
    """
    A simple context manager (and decorator) class useful
    in tests which is necessary to change some
    setting in the safe way
    """

    def __init__(self, **kwargs):
        self.new_settings = kwargs
        self.old_settings = {}

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner

    def __enter__(self):
        settings.setup()
        for key, value in self.new_settings.items():
            if key not in settings._dict:
                raise ValueError(
                    'Your current settings do not '
                    'have a setting {}'.format(key)
                )
            self.old_settings[key] = settings._dict[key]
            settings._dict[key] = value

    def __exit__(self, ext_type, exc_value, traceback):
        for key, value in self.old_settings.items():
            settings._dict[key] = value
