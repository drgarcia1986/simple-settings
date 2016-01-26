# -*- coding: utf-8 -*-
import codecs


class SettingsLoadStrategyCfg(object):

    name = 'cfg'

    def is_valid_file(self, file_name):
        return file_name.endswith('.cfg')

    def load_settings_file(self, settings_file):
        result = {}
        with codecs.open(settings_file, 'r', 'utf-8') as f:
            settings = [
                line.split('=') for line in f if self._is_valid_line(line)
            ]
            for k, v in settings:
                result[k.strip()] = v.strip()
        return result

    def _is_valid_line(self, line):
        clean_line = line.strip()
        return bool(
            clean_line
            and not clean_line.startswith('#')
            and len(clean_line.split('=')) == 2
        )
