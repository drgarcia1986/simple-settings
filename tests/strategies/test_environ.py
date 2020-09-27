import os

import pytest

from simple_settings.strategies.environ import SettingsLoadStrategyEnviron


class TestEnvironStrategy:

    @pytest.fixture
    def strategy_environ(self):
        return SettingsLoadStrategyEnviron

    def test_should_check_a_valid_environ_file(self, strategy_environ):
        assert strategy_environ.is_valid_file('foo.environ') is True

    def test_should_check_a_invalid_environ_file(self, strategy_environ):
        assert strategy_environ.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_environ_file(self, strategy_environ):
        settings = strategy_environ.load_settings_file(
            '.environ'
        )

        for k, v in os.environ.items():
            assert settings[k] == v

    def test_should_load_dict_with_settings_of_prefixed_environ_file(self, strategy_environ):
        os.environ.update(dict(
            PREFIX_A='good',
            PREFIX_13='great',
            WRONG_PREFIX_XYZ='1',
        ))
        settings = strategy_environ.load_settings_file(
            'PREFIX_.environ'
        )

        assert settings['PREFIX_A'] == 'good'
        assert settings['PREFIX_13'] == 'great'

        assert 'WRONG_PREFIX_XYZ' not in settings
