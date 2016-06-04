# -*- coding: utf-8 -*-
from functools import wraps

from .core import settings


class SettingsStub(object):
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
        self.old_settings = settings.as_dict()
        settings.configure(**self.new_settings)

    def __exit__(self, ext_type, exc_value, traceback):
        settings.configure(**self.old_settings)


settings_stub = SettingsStub
