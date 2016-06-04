# -*- coding: utf-8 -*-
import sys

import pytest
from mock import patch

from simple_settings.core import LazySettings
from simple_settings.special_settings import SPECIAL_SETTINGS_KEY


def get_settings_by_cmd_line(module_name):
    settings = LazySettings()

    with patch.object(
        sys, 'argv', ['', '--settings={}'.format(module_name)]
    ):
        settings.setup()

    return settings


def get_settings_by_environment(module_name):
    settings = LazySettings()
    mock_dict = {
        key: module_name for key in LazySettings.ENVIRON_KEYS
    }
    with patch.dict('os.environ', mock_dict):
        settings.setup()

    return settings


class TestSettings(object):

    def test_should_read_init_settings_value(self):
        expect_module = 'tests.samples.simple'
        settings = LazySettings(expect_module)

        assert settings._settings_list == [expect_module]
        assert settings.SIMPLE_STRING == u'simple'

    def test_should_return_a_nice_repr(self):
        settings = LazySettings('tests.samples.simple')

        assert repr(settings) == '<SIMPLE-SETTINGS ({})>'.format(
            settings.as_dict()
        )

    def test_should_read_init_multiples_settings_value(self):
        expect_modules = 'tests.samples.simple,tests.samples.complex'
        settings = LazySettings(*expect_modules.split(','))

        assert settings._settings_list == expect_modules.split(',')
        assert settings.SIMPLE_STRING == u'simple'
        assert settings.COMPLEX_DICT['complex'] == 'settings'

    @pytest.mark.parametrize('cmd_arg', LazySettings.COMMAND_LINE_ARGS)
    def test_should_read_cmd_line_settings_value(self, cmd_arg):
        expect_module = 'tests.samples.simple'

        settings = LazySettings()
        with patch.object(
            sys, 'argv', ['', '{}={}'.format(cmd_arg, expect_module)]
        ):
            settings.setup()

        assert settings._settings_list == [expect_module]

    def test_should_read_cmd_line_multiples_settings_value(self):
        expect_modules = 'tests.samples.simple,tests.samples.complex'
        settings = get_settings_by_cmd_line(expect_modules)

        assert settings._settings_list == expect_modules.split(',')

    @pytest.mark.parametrize('env_var', LazySettings.ENVIRON_KEYS)
    def test_should_read_environment_settings_value(self, env_var):
        expect_module = 'tests.samples.complex'

        settings = LazySettings()
        with patch.object(sys, 'argv', []):
            with patch.dict('os.environ', {env_var: expect_module}):
                settings.setup()

        assert settings._settings_list == [expect_module]

    def test_should_read_environment_multiples_settings_value(self):
        expect_modules = 'tests.samples.complex,tests.samples.complex'
        with patch.object(sys, 'argv', []):
            settings = get_settings_by_environment(expect_modules)

        assert settings._settings_list == expect_modules.split(',')

    def test_should_load_a_simple_module_settings(self):
        settings = get_settings_by_cmd_line('tests.samples.simple')

        assert settings.SIMPLE_STRING == u'simple'
        assert settings.SIMPLE_INTEGER == 1

    def test_should_inherit_settings(self):
        settings = get_settings_by_cmd_line('tests.samples.simple')

        assert settings.APPLICATION_NAME == u'Simple Settings'

    def test_should_load_multiple_settings_by_pipeline(self):
        settings = get_settings_by_cmd_line(
            'tests.samples.simple,tests.samples.without_import'
        )

        assert settings.SIMPLE_STRING == u'simple'
        assert settings.SOME_TEXT == u'some text'

    def test_should_inherit_settings_with_pipeline(self):
        settings = get_settings_by_cmd_line(
            'tests.samples.simple,tests.samples.without_import'
        )

        assert settings.SIMPLE_INTEGER == 2

    def test_should_load_a_complex_module_settings(self):
        settings = get_settings_by_cmd_line('tests.samples.complex')

        assert settings.COMPLEX_DICT['complex'] == 'settings'
        assert settings.COMPLEX_DICT['foo'] == 'bar'

    def test_should_read_settings_by_method_as_dict(self):
        settings = get_settings_by_cmd_line('tests.samples.simple')

        expected_dict = {
            'APPLICATION_NAME': u'Simple Settings',
            'SIMPLE_STRING': u'simple',
            'SIMPLE_INTEGER': 1
        }
        assert settings.as_dict() == expected_dict

    def test_as_dict_should_keep_settings_if_change_a_mutable_variable(self):
        settings = get_settings_by_cmd_line('tests.samples.complex')

        settings_dict = settings.as_dict()
        settings_dict['COMPLEX_DICT']['complex'] = 'barz'

        assert settings.COMPLEX_DICT['complex'] == 'settings'

    def test_dont_import_a_module_as_setting(self):
        settings = get_settings_by_cmd_line(
            'tests.samples.with_module_imported'
        )

        assert 'os' not in settings.as_dict()

    def test_dont_overwrite_special_settings_with_environ(self):
        expect_module = 'tests.samples.special'

        settings = LazySettings()
        with patch.object(sys, 'argv', []):
            with patch.dict('os.environ', {SPECIAL_SETTINGS_KEY: expect_module}):
                settings.setup()

        print(settings.as_dict())
        assert isinstance(getattr(settings, SPECIAL_SETTINGS_KEY), dict)

    def test_should_configure_settings_with_new_values(self):
        settings = LazySettings('tests.samples.simple')

        assert settings.SIMPLE_STRING == 'simple'
        settings.configure(SIMPLE_STRING='simple2')
        assert settings.SIMPLE_STRING == 'simple2'

        settings.configure(NEW_VALUE='new')
        assert settings.NEW_VALUE == 'new'

    def test_should_load_settings_by_cfg_file(self):
        settings = get_settings_by_cmd_line('tests/samples/key_value.cfg')

        assert settings.SIMPLE_STRING == 'simple'
        assert settings.TWO_WORDS == 'no problem'
        assert settings.AFTER_LINEBREAK == 'ok'
        assert settings.WITH_UTF8_CHAR == u'café'

        with pytest.raises(AttributeError):
            settings.COMMENTARY

    def test_should_raise_error_if_setting_are_not_configured(self):
        settings = LazySettings()
        with patch.object(sys, 'argv', []):
            with pytest.raises(RuntimeError):
                settings.foo

    def test_should_raise_error_if_setting_configured_wrong(self):
        settings = LazySettings()
        with patch.object(
            sys, 'argv', ['', '--settings', 'tests.samples.simple']
        ):
            with pytest.raises(RuntimeError):
                settings.foo

    def test_should_raise_error_if_setting_not_found(self):
        settings = LazySettings()
        with patch.object(sys, 'argv', ['', '--settings=foo']):
            with pytest.raises(RuntimeError):
                settings.foo

    def test_should_raise_error_if_dont_have_strategy_for_an_file(self):
        settings = LazySettings()
        with patch.object(sys, 'argv', ['', '--settings=foo.bar']):
            with pytest.raises(RuntimeError):
                settings.foo

    def test_should_setup_setting_only_once(self):
        settings = get_settings_by_cmd_line('tests.samples.simple')
        with patch.object(settings, '_get_settings_from_cmd_line') as mock:
            settings.SIMPLE_STRING

        assert not mock.called
