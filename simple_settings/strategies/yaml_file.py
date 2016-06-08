# -*- coding: utf-8 -*-
import codecs

import yaml


class SettingsLoadStrategyYaml(object):
    """
    This is the strategy used to read settings from yaml files
    """
    name = 'yaml'

    @staticmethod
    def is_valid_file(file_name):
        return file_name.endswith('.yaml') or file_name.endswith('.yml')

    @staticmethod
    def load_settings_file(settings_file):
        with codecs.open(settings_file, 'r') as f:
            return yaml.safe_load(f)
