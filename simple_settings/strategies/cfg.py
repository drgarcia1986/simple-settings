# -*- coding: utf-8 -*-
import codecs
import os
from .types import SettingsLoadStrategy


def _is_cfg_file(file_name):
    return file_name.endswith('.cfg')


def _load_cfg_file(settings_file):
    def is_valid_line(line):
        clean_line = line.strip()
        return bool(
            clean_line
            and not clean_line.startswith('#')
            and len(clean_line.split('=')) == 2
        )

    result = {}
    with codecs.open(settings_file, 'r', 'utf-8') as f:
        for line in f:
            if is_valid_line(line):
                setting, value = [i.strip() for i in line.split('=')]
                result[setting] = os.environ.get(setting, value)
    return result


strategy = SettingsLoadStrategy(
    name='cfg',
    is_valid_file=_is_cfg_file,
    load_settings_file=_load_cfg_file
)
