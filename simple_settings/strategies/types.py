from collections import namedtuple


SettingsLoadStrategy = namedtuple(
    'strategy',
    [
        'name',
        'is_valid_file',
        'load_settings_file'
    ]
)
