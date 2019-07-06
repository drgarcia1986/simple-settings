# -*- coding: utf-8 -*-
import os


class SettingsLoadStrategyEnviron(object):
    """
    This is the strategy used to read settings from `os.environ`.
    `file_name` could be '.environ' to load all environment variables or
    '`PREFIX`.environ' to load environment variables starting with `PREFIX`.
    """
    name = 'environ'

    @staticmethod
    def is_valid_file(file_name):
        return file_name.endswith('.environ')

    @staticmethod
    def load_settings_file(settings_file):
        env_prefix = settings_file.replace('.environ', '')
        if env_prefix:
            result = {}
            for k, v in os.environ.items():
                if k.startswith(env_prefix):
                    result[k] = v
        else:
            result = os.environ.copy()
        return result
