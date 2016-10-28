# -*- coding: utf-8 -*-
import pytest

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import get_dynamic_reader

skip = False
try:
    import six
    from redis import StrictRedis
    from simple_settings.dynamic_settings.redis_reader import (
        Reader as RedisReader
    )
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
            'SIMPLE_STRING': 'simple'
        }

    @pytest.yield_fixture
    def redis(self):
        redis = StrictRedis()

        yield redis

        redis.flushall()

    @pytest.fixture
    def reader(self, settings_dict_to_override_by_redis):
        return get_dynamic_reader(settings_dict_to_override_by_redis)

    def _get_value_from_redis(self, redis, key):
        result = redis.get(key)
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')
        return result

    def test_should_return_an_instance_of_redis_reader(
        self, settings_dict_to_override_by_redis
    ):
        reader = get_dynamic_reader(settings_dict_to_override_by_redis)
        assert isinstance(reader, RedisReader)

    def test_should_get_string_in_redis_by_reader(self, redis, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from redis'
        redis.set(key, expected_setting)

        assert reader.get(key) == expected_setting

    def test_should_set_string_in_redis_by_reader(self, redis, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from redis'
        reader.set(key, expected_setting)

        assert self._get_value_from_redis(redis, key) == expected_setting

    def test_should_use_redis_reader_with_simple_settings(self, redis):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'redis'}}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        redis.set('SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert self._get_value_from_redis(redis, 'SIMPLE_STRING') == 'foo'

    def test_should_use_redis_reader_with_prefix_with_simple_settings(self, redis):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': {'backend': 'redis', 'prefix': 'MYAPP_'}}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        redis.set('MYAPP_SIMPLE_STRING', 'dynamic')
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert self._get_value_from_redis(redis, 'MYAPP_SIMPLE_STRING') == 'foo'
