# -*- coding: utf-8 -*-
import pytest

skip = False
try:
    from simple_settings.strategies.toml_file import SettingsLoadStrategyToml
except ImportError:
    skip = True


@pytest.mark.skipif(skip, reason='Installed without Toml')
class TestTomlStrategy(object):

    @pytest.fixture
    def strategy_toml(self):
        return SettingsLoadStrategyToml

    def test_should_check_a_valid_toml_file(self, strategy_toml):
        assert strategy_toml.is_valid_file('foo.toml') is True

    def test_should_check_a_invalid_toml_file(self, strategy_toml):
        assert strategy_toml.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_toml_file(self, strategy_toml):
        settings = strategy_toml.load_settings_file(
            'tests/samples/simple_toml_file.toml'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
        assert settings['COMPLEX_DICT'] == {'complex': 'dict', 'foo': 'bar'}
        assert settings['COMPLEX_LIST'] == ['foo', 'bar']
        assert settings['SIMPLE_INTEGER'] == 1
        assert settings['SIMPLE_BOOL'] is True
