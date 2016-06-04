# -*- coding: utf-8 -*-
import codecs
import json


class SettingsLoadStrategyJson(object):
    """
    This is the strategy used to read settings from json files
    """
    name = 'json'

    @classmethod
    def is_valid_file(cls, file_name):
        return file_name.endswith('.json')

    @classmethod
    def load_settings_file(cls, settings_file):
        with codecs.open(settings_file, 'r') as f:
            return json.loads(f.read())
