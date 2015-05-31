from collections import namedtuple


SettingsStrategy = namedtuple(
    'strategy',
    [
        'name',
        'is_valid_file',
        'load_settings_file'
    ]
)
