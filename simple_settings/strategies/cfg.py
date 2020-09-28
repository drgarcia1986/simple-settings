import codecs


class SettingsLoadStrategyCfg:
    """
    This is the strategy used to read settings from cfg files
    (simple `key=value` files)
    """
    name = 'cfg'

    @staticmethod
    def is_valid_file(file_name):
        return file_name.endswith('.cfg')

    @classmethod
    def load_settings_file(cls, settings_file):
        result = {}
        with codecs.open(settings_file, 'r', 'utf-8') as f:
            settings = [
                line.split('=') for line in f if cls._is_valid_line(line)
            ]
            for k, v in settings:
                result[k.strip()] = v.strip()
        return result

    @staticmethod
    def _is_valid_line(line):
        clean_line = line.strip()
        return bool(
            clean_line and not
            clean_line.startswith('#') and
            len(clean_line.split('=')) == 2
        )
