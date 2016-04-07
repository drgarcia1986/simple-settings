import pytest
from mock import MagicMock, patch

from simple_settings.special_settings import (
    override_settings_by_env,
    process_special_settings,
    required_settings,
    SPECIAL_SETTINGS_MAPPING,
)


class TestSpecialSettings(object):

    @pytest.fixture
    def settings_dict_to_override(self):
        return {
            'SIMPLE_SETTINGS': {'OVERRIDE_BY_ENV': True},
            'SIMPLE_STRING': 'simple',
            'SIMPLE_INTEGER': 1
        }

    @pytest.fixture
    def settings_dict_required(self):
        return {'SIMPLE_SETTINGS': {
            'REQUIRED_SETTINGS': ('SIMPLE_STRING', 'LOST_SETTING')
        }}

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

        assert 'LOST_SETTING' in str(exc)

    def test_should_call_functions_in_process_special_settings(self):
        mock = MagicMock()
        settings_dict = {'SIMPLE_SETTINGS': {'foo': mock}}
        with patch.dict(SPECIAL_SETTINGS_MAPPING, {'foo': mock}):
            process_special_settings(settings_dict)

        assert mock.called
