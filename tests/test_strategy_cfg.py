# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def cfg_strategy():
    from simple_settings.strategies import cfg
    return cfg.strategy


class TestCfgStrategy(object):

    def test_should_check_a_valid_cfg_file(self, cfg_strategy):
        assert cfg_strategy.is_valid_file('foo.cfg') is True

    def test_should_check_a_invalid_cfg_file(self, cfg_strategy):
        assert cfg_strategy.is_valid_file('foo.bar') is False

    def test_should_load_dict_with_settings_of_cfg_file(self, cfg_strategy):
        settings = cfg_strategy.load_settings_file(
            'tests/samples/key_value.cfg'
        )

        assert settings['SIMPLE_STRING'] == 'simple'
