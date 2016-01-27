# -*- coding: utf-8 -*-
import pytest

from simple_settings.strategies.cfg import SettingsLoadStrategyCfg


class TestCfgStrategy(object):

    @pytest.fixture
    def strategy_cfg(self):
        return SettingsLoadStrategyCfg

    def test_should_check_a_valid_cfg_file(self, strategy_cfg):
        assert strategy_cfg.is_valid_file('foo.cfg') is True

    def test_should_check_a_invalid_cfg_file(self, strategy_cfg):
        assert strategy_cfg.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_cfg_file(self, strategy_cfg):
        settings = strategy_cfg.load_settings_file(
            'tests/samples/key_value.cfg'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
