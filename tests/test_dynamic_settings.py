# -*- coding: utf-8 -*-
import pytest

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import process_dynamic_settings

skip = False
try:
    from redis import StrictRedis
except ImportError:
    skip = True


@pytest.mark.skipif(skip, reason='Installed without redis')
class TestDynamicRedisSettings(object):

    @pytest.fixture
    def settings_dict_to_override_by_redis(self):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': {'backend': 'redis'}
            },
            'SIMPLE_STRING': 'simple',
        }

    @pytest.yield_fixture
    def redis(self):
        redis = StrictRedis()

        yield redis

        redis.flushall()

    def test_should_return_none_for_setting_without_redis_key(
        self, settings_dict_to_override_by_redis
    ):
        assert process_dynamic_settings(
            settings_dict_to_override_by_redis, 'SIMPLE_STRING'
        ) is None

    def test_should_override_by_redis(
        self, settings_dict_to_override_by_redis, redis
    ):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from env'
        redis.set(key, expected_setting)

        assert process_dynamic_settings(
            settings_dict_to_override_by_redis, key
        ) == expected_setting

    def test_should_get_dynamic_setting_by_env(self, redis):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'redis'}}
        )

        assert settings.SIMPLE_STRING == 'simple'

        redis.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        redis.delete('SIMPLE_STRING')
        assert settings.SIMPLE_STRING == 'simple'
