from collections import OrderedDict
from unittest.mock import MagicMock, call, patch

import pytest

from simple_settings.special_settings import (
    configure_logging,
    override_settings_by_env,
    process_special_settings,
    required_not_none_settings,
    required_settings,
    required_settings_types
)


class TestSpecialSettings:
    @pytest.fixture
    def settings_dict_to_override(self):
        return {
            'SIMPLE_SETTINGS': {
                'OVERRIDE_BY_ENV': True
            },
            'SIMPLE_STRING': 'simple',
            'SIMPLE_INTEGER': 1
        }

    @pytest.fixture
    def settings_dict_required(self):
        return {
            'SIMPLE_SETTINGS': {
                'REQUIRED_SETTINGS': ('SIMPLE_STRING', 'LOST_SETTING')
            },
            'SIMPLE_STRING': None,
        }

    @pytest.fixture
    def settings_dict_required_not_none(self):
        return {
            'SIMPLE_SETTINGS': {
                'REQUIRED_NOT_NONE_SETTINGS': ('SIMPLE_STRING', )
            },
            'SIMPLE_STRING': None,
            'SIMPLE_INTEGER': None
        }

    @pytest.fixture
    def settings_dict_required_types_unsupported_type(self):
        return {
            'SIMPLE_SETTINGS': {
                'REQUIRED_SETTINGS_TYPES': {
                    'SIMPLE_STRING': 'str',
                    'UNSUPPORTED_TYPE': 'foo'
                }
            }
        }

    @pytest.fixture
    def settings_dict_required_types_invalid_types(self):
        return {
            'SIMPLE_SETTINGS': {
                'REQUIRED_SETTINGS_TYPES': {
                    'SIMPLE_INTEGER': 'int',
                    'SIMPLE_BOOL': 'bool',
                    'SIMPLE_STR': 'json.loads',
                }
            },
            'SIMPLE_INTEGER': 0.1,  # not an int and not a str so cannot parse
            'SIMPLE_BOOL': 'foo',  # not a bool and not parseable to a bool
            'SIMPLE_STR': 'foo',  # not a valid value to perform json.loads
        }

    @pytest.fixture
    def settings_dict_required_types_valid_types(self):
        return {
            'SIMPLE_SETTINGS': {
                'REQUIRED_SETTINGS_TYPES': {
                    'STRING_NONE': 'str',
                    'STRING_NATIVE': 'str',
                    'INTEGER_NONE': 'int',
                    'INTEGER_NATIVE': 'int',
                    'INTEGER_PARSED': 'int',
                    'FLOAT_NONE': 'float',
                    'FLOAT_NATIVE': 'float',
                    'FLOAT_PARSED': 'float',
                    'BOOL_NONE': 'bool',
                    'BOOL_NATIVE': 'bool',
                    'BOOL_PARSED_1': 'bool',
                    'BOOL_PARSED_3': 'bool',
                    'BOOL_PARSED_4': 'bool',
                    'BOOL_PARSED_5': 'bool',
                    'JSON_LOADS_PARSED_1': 'json.loads',
                    'JSON_LOADS_PARSED_2': 'json.loads',
                    'JSON_LOADS_PARSED_3': 'json.loads',
                    'JSON_LOADS_PARSED_4': 'json.loads',
                    'JSON_LOADS_PARSED_5': 'json.loads',
                    'JSON_LOADS_PARSED_6': 'json.loads',
                }
            },
            'STRING_NONE': None,
            'STRING_NATIVE': 'simple',
            'INTEGER_NONE': None,
            'INTEGER_NATIVE': 2,
            'INTEGER_PARSED': '3',
            'FLOAT_NONE': None,
            'FLOAT_NATIVE': 0.2,
            'FLOAT_PARSED': '0.3',
            'BOOL_NONE': None,
            'BOOL_NATIVE': True,
            'BOOL_PARSED_1': 'true',
            'BOOL_PARSED_3': 'True',
            'BOOL_PARSED_4': 'false',
            'BOOL_PARSED_5': 'False',
            'JSON_LOADS_PARSED_1': '{"simple": "value"}',
            'JSON_LOADS_PARSED_2': 'true',
            'JSON_LOADS_PARSED_3': '1',
            'JSON_LOADS_PARSED_4': [1, 3],
            'JSON_LOADS_PARSED_5': '[1, 3]',
            'JSON_LOADS_PARSED_6': {"simple": "value"},
        }

    @pytest.fixture
    def settings_dict_override_and_required(self):
        return {
            'SIMPLE_SETTINGS': {
                'OVERRIDE_BY_ENV': True,
                'REQUIRED_SETTINGS': ('SIMPLE_INTEGER', ),
                'REQUIRED_NOT_NONE_SETTINGS': ('SIMPLE_INTEGER', ),
                'REQUIRED_SETTINGS_TYPES': {
                    'SIMPLE_INTEGER': 'int'
                }
            },
            'SIMPLE_INTEGER': None
        }

    @pytest.fixture
    def settings_dict_logging(self):
        return {
            'SIMPLE_SETTINGS': {
                'CONFIGURE_LOGGING': True
            },
            'LOGGING': {
                'dummy': 'dict'
            }
        }

    def test_should_autoconfig_python_logging(self, settings_dict_logging):
        with patch('logging.config.dictConfig') as mock:
            configure_logging(settings_dict_logging)
        mock.assert_called_once_with(settings_dict_logging['LOGGING'])

    def test_should_dont_autoconfig_python_logging_if_dont_have_special_key(
        self, settings_dict_logging
    ):
        settings_dict_logging['SIMPLE_SETTINGS']['CONFIGURE_LOGGING'] = False
        with patch('logging.config.dictConfig') as mock:
            configure_logging(settings_dict_logging)
        assert not mock.called

    def test_should_override_by_env(self, settings_dict_to_override):
        def mock_env_side_effect(k, d=None):
            return u'simple from env' if k == 'SIMPLE_STRING' else d

        with patch('os.environ.get', side_effect=mock_env_side_effect):
            override_settings_by_env(settings_dict_to_override)

        assert settings_dict_to_override['SIMPLE_STRING'] == u'simple from env'
        assert settings_dict_to_override['SIMPLE_INTEGER'] == 1

    def test_should_dont_override_by_env_if_settings_dont_have_special_key(
        self, settings_dict_to_override
    ):
        def mock_env_side_effect(k, d=None):
            return u'simple from env' if k == 'SIMPLE_STRING' else d

        settings_dict_to_override['SIMPLE_SETTINGS']['OVERRIDE_BY_ENV'] = False
        with patch('os.environ.get', side_effect=mock_env_side_effect):
            override_settings_by_env(settings_dict_to_override)

        assert settings_dict_to_override['SIMPLE_STRING'] == u'simple'

    def test_required_settings_should_raise_value_error_for_a_lost_setting(
        self, settings_dict_required
    ):
        with pytest.raises(ValueError) as exc:
            required_settings(settings_dict_required)

        assert 'LOST_SETTING' in str(exc.value)
        assert 'SIMPLE_STRING' not in str(exc.value)

    def test_required_not_none_settings_should_raise_value_error_for_a_none_setting(
        self, settings_dict_required_not_none
    ):
        with pytest.raises(ValueError) as exc:
            required_not_none_settings(settings_dict_required_not_none)

        assert 'SIMPLE_STRING' in str(exc.value)
        assert 'SIMPLE_INTEGER' not in str(exc.value)

    def test_required_settings_types_should_raise_value_error_for_an_unsupported_type(
        self, settings_dict_required_types_unsupported_type
    ):
        with pytest.raises(ValueError) as exc:
            required_settings_types(
                settings_dict_required_types_unsupported_type
            )

        assert 'UNSUPPORTED_TYPE' in str(exc.value)
        assert 'SIMPLE_INTEGER' not in str(exc.value)

    def test_required_settings_types_should_raise_value_error_for_invalid_types(
        self, settings_dict_required_types_invalid_types
    ):
        with pytest.raises(ValueError) as exc:
            required_settings_types(settings_dict_required_types_invalid_types)

        assert 'SIMPLE_INTEGER' in str(exc.value)
        assert 'SIMPLE_BOOL' in str(exc.value)

    def test_required_settings_types_should_not_raise_value_error_for_valid_types(
        self, settings_dict_required_types_valid_types
    ):
        required_settings_types(settings_dict_required_types_valid_types)

        def converted_value(key):
            return settings_dict_required_types_valid_types[key]

        assert converted_value('STRING_NONE') is None
        assert converted_value('INTEGER_NONE') is None
        assert converted_value('FLOAT_NONE') is None
        assert converted_value('BOOL_NONE') is None

        assert isinstance(converted_value('STRING_NATIVE'), str)
        assert isinstance(converted_value('INTEGER_NATIVE'), int)
        assert isinstance(converted_value('INTEGER_PARSED'), int)
        assert isinstance(converted_value('FLOAT_NATIVE'), float)
        assert isinstance(converted_value('FLOAT_PARSED'), float)
        assert isinstance(converted_value('BOOL_NATIVE'), bool)
        assert isinstance(converted_value('BOOL_PARSED_1'), bool)
        assert isinstance(converted_value('BOOL_PARSED_3'), bool)
        assert isinstance(converted_value('BOOL_PARSED_4'), bool)
        assert isinstance(converted_value('BOOL_PARSED_5'), bool)
        assert isinstance(converted_value('JSON_LOADS_PARSED_1'), dict)
        assert isinstance(converted_value('JSON_LOADS_PARSED_2'), bool)
        assert isinstance(converted_value('JSON_LOADS_PARSED_3'), int)

        assert converted_value('JSON_LOADS_PARSED_1') == {'simple': 'value'}
        assert converted_value('JSON_LOADS_PARSED_2') is True
        assert converted_value('JSON_LOADS_PARSED_3') == 1
        assert converted_value('JSON_LOADS_PARSED_4') == [1, 3]
        assert converted_value('JSON_LOADS_PARSED_5') == [1, 3]
        assert converted_value('JSON_LOADS_PARSED_6') == {'simple': 'value'}

    def test_override_by_env_and_required_loads_in_correct_order(
        self, settings_dict_override_and_required
    ):
        def mock_env_side_effect(k, d=None):
            return '1' if k == 'SIMPLE_INTEGER' else d

        with patch('os.environ.get', side_effect=mock_env_side_effect):
            process_special_settings(settings_dict_override_and_required)

        assert settings_dict_override_and_required['SIMPLE_INTEGER'] == 1

    def test_should_call_functions_in_process_special_settings(self):
        funcs = MagicMock()

        settings_dict = {
            'SIMPLE_SETTINGS': {
                'bar': 'bar_value',
                'foo': 'foo_value'
            }
        }

        with patch(
            'simple_settings.special_settings.SPECIAL_SETTINGS_MAPPING',
            OrderedDict((('foo', funcs.foo), ('bar', funcs.bar)))
        ):
            process_special_settings(settings_dict)

        assert funcs.mock_calls == [
            call.foo(settings_dict),
            call.bar(settings_dict)
        ]
