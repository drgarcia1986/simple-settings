# -*- coding: utf-8 -*-
import codecs

import toml


class SettingsLoadStrategyToml(object):
    """
    This is the strategy used to read settings from toml files
    """
    name = 'toml'

    @staticmethod
    def is_valid_file(file_name):
        return file_name.endswith('.toml')

    @staticmethod
    def load_settings_file(settings_file):
        with codecs.open(settings_file, 'r') as f:
            return toml.loads(f.read())
