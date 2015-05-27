# -*- coding: utf-8 -*-
import sys
from mock import patch
import pytest


def get_settings_by_cmd_line(module_name):
    with patch.object(
        sys, 'argv', ['', '--settings={}'.format(module_name)]
    ):
        from simple_settings.core import _Settings
        return _Settings()


def get_settings_by_environment(module_name):
    with patch('os.environ.get') as mock:
        mock.return_value = module_name
        from simple_settings.core import _Settings
        return _Settings()


class TestSettings(object):

    def test_should_read_cmd_line_settings_value(self):
        expect_module = 'tests.samples.simple'
        settings = get_settings_by_cmd_line(expect_module)

        assert settings._settings_list == [expect_module]

    def test_should_read_cmd_line_multiples_settings_value(self):
        expect_modules = 'tests.samples.simple,tests.samples.complex'
        settings = get_settings_by_cmd_line(expect_modules)

        assert settings._settings_list == expect_modules.split(',')

    def test_should_read_environment_settings_value(self):
        expect_module = 'tests.samples.complex'
        with patch.object(sys, 'argv', []):
            settings = get_settings_by_environment(expect_module)

        assert settings._settings_list == [expect_module]

    def test_should_read_environment_multiples_settings_value(self):
        expect_modules = 'tests.samples.complex,tests.samples.complex'
        with patch.object(sys, 'argv', []):
            settings = get_settings_by_environment(expect_modules)

        assert settings._settings_list == expect_modules.split(',')

    def test_load_a_simple_module_settings(self):
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

    def test_load_a_complex_module_settings(self):
        settings = get_settings_by_cmd_line('tests.samples.complex')

        assert settings.COMPLEX_DICT['complex'] == 'settings'
        assert settings.COMPLEX_DICT['foo'] == 'bar'

    def test_read_settings_by_method_as_dict(self):
        settings = get_settings_by_cmd_line('tests.samples.simple')

        settings_dict = settings.as_dict()
        assert settings_dict['SIMPLE_STRING'] == u'simple'
        assert settings_dict['SIMPLE_INTEGER'] == 1

    def test_setting_override_by_environment(self):
        def _mock_env_side_effect(k, d=None):
            return u'simple from env' if k == 'SIMPLE_STRING' else d

        with patch('os.environ.get', side_effect=_mock_env_side_effect):
            settings = get_settings_by_cmd_line('tests.samples.simple')

        assert settings.SIMPLE_STRING == u'simple from env'

    def test_setting_are_not_configured(self):
        with patch.object(sys, 'argv', []):
            with pytest.raises(RuntimeError):
                from simple_settings.core import _Settings
                _Settings()

    def test_setting_configured_wrong(self):
        with patch.object(
            sys, 'argv', ['', '--settings', 'tests.samples.simple']
        ):
            with pytest.raises(RuntimeError):
                from simple_settings.core import _Settings
                _Settings()

    def test_setting_not_found(self):
        with patch.object(sys, 'argv', ['', '--settings=foo']):
            with pytest.raises(ImportError):
                from simple_settings.core import _Settings
                _Settings()
