# -*- coding: utf-8 -*-
import pytest
from mock import MagicMock, patch

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import process_dynamic_settings


class TestDynamicSettings(object):

    @pytest.fixture
    def settings_dict_to_override_by_env(self):
        return {
            'DYNAMIC_SETTINGS': ['ENV'],
            'SIMPLE_STRING': 'simple',
        }

    def test_should_return_none_for_setting_without_env(
        self, settings_dict_to_override_by_env
    ):
        assert process_dynamic_settings(
            settings_dict_to_override_by_env, 'SIMPLE_STRING'
        ) is None


    def test_should_override_by_env(self, settings_dict_to_override_by_env):
        expected_setting = 'simple from env'
        def mock_env_side_effect(k, d=None):
            return expected_setting if k == 'SIMPLE_STRING' else d

        with patch('os.environ.get', side_effect=mock_env_side_effect):
            assert process_dynamic_settings(
                settings_dict_to_override_by_env, 'SIMPLE_STRING'
            ) == expected_setting

    def test_should_get_dynamic_setting_by_env(self):
        settings = LazySettings('tests.samples.simple')
        settings.configure(DYNAMIC_SETTINGS=['ENV'])

        assert settings.SIMPLE_STRING == 'simple'

        def mock_env_side_effect(k, d=None):
            return 'dynamic' if k == 'SIMPLE_STRING' else d

        with patch('os.environ.get', side_effect=mock_env_side_effect):
            assert settings.SIMPLE_STRING == 'dynamic'
        assert settings.SIMPLE_STRING == 'simple'
