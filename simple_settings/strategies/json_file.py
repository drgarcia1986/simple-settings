# -*- coding: utf-8 -*-
import codecs
import json


class SettingsLoadStrategyJson(object):
    """
    This is the strategy used to read settings from json files
    """
    name = 'json'

    @staticmethod
    def is_valid_file(file_name):
        return file_name.endswith('.json')

    @staticmethod
    def load_settings_file(settings_file):
        with codecs.open(settings_file, 'r') as f:
            return json.loads(f.read())
