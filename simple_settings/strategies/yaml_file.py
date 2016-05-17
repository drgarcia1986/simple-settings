# -*- coding: utf-8 -*-
import codecs

import yaml


class SettingsLoadStrategyYaml(object):
    """
    This is the strategy used to read settings from yaml files
    """
    name = 'yaml'

    @classmethod
    def is_valid_file(cls, file_name):
        return file_name.endswith('.yaml') or file_name.endswith('.yml')

    @classmethod
    def load_settings_file(cls, settings_file):
        with codecs.open(settings_file, 'r') as f:
            return yaml.safe_load(f)
