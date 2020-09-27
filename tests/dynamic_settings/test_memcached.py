import pytest

from simple_settings.core import LazySettings
from simple_settings.dynamic_settings import get_dynamic_reader

skip = False
try:
    import six
    from pymemcache.client.base import Client

    from simple_settings.dynamic_settings.memcached_reader import \
        Reader as MemcachedReader
except ImportError:
    skip = True


@pytest.mark.skipif(skip, reason='Installed without pymemcache')
class TestDynamicMemcachedSettings:

    @pytest.fixture
    def host(self):
        return 'localhost'

    @pytest.fixture
    def port(self):
        return 11211

    @pytest.fixture
    def dynamic_settings(self, host, port):
        return {
            'backend': 'memcached',
            'host': host,
            'port': port
        }

    @pytest.fixture
    def settings_dict_to_override_by_memcached(self, dynamic_settings):
        return {
            'SIMPLE_SETTINGS': {
                'DYNAMIC_SETTINGS': dynamic_settings
            },
            'SIMPLE_STRING': 'simple'
        }

    @pytest.fixture
    def memcached(self, host, port):
        memcached = Client((host, port))

        yield memcached

        memcached.flush_all()

    @pytest.fixture
    def reader(self, settings_dict_to_override_by_memcached):
        return get_dynamic_reader(settings_dict_to_override_by_memcached)

    def _get_value_from_memcached(self, memcached, key):
        result = memcached.get(key)
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')

        return result

    def test_should_return_an_instance_of_memcached_reader(
        self, settings_dict_to_override_by_memcached
    ):
        reader = get_dynamic_reader(settings_dict_to_override_by_memcached)
        assert isinstance(reader, MemcachedReader)

    def test_should_get_string_in_memcached_by_reader(self, memcached, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from memcached'
        memcached.set(key, expected_setting, noreply=False)

        assert reader.get(key) == expected_setting

    def test_should_set_string_in_memcached_by_reader(self, memcached, reader):
        key = 'SIMPLE_STRING'
        expected_setting = 'simple from memcached'
        reader.set(key, expected_setting)

        assert self._get_value_from_memcached(
            memcached,
            key
        ) == expected_setting

    def test_should_use_memcached_reader_with_simple_settings(
        self,
        memcached,
        dynamic_settings
    ):
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': dynamic_settings}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        memcached.set('SIMPLE_STRING', 'dynamic', noreply=False)
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert self._get_value_from_memcached(
            memcached,
            'SIMPLE_STRING'
        ) == 'foo'

    def test_should_use_memcached_reader_with_prefix(
        self,
        memcached,
        dynamic_settings
    ):
        dynamic_settings['prefix'] = 'MYAPP_'
        settings = LazySettings('tests.samples.simple')
        settings.configure(
            SIMPLE_SETTINGS={'DYNAMIC_SETTINGS': dynamic_settings}
        )
        settings._initialized = False
        settings.setup()

        assert settings.SIMPLE_STRING == 'simple'

        memcached.set('MYAPP_SIMPLE_STRING', 'dynamic', noreply=False)
        assert settings.SIMPLE_STRING == 'dynamic'

        settings.configure(SIMPLE_STRING='foo')
        assert self._get_value_from_memcached(
            memcached,
            'MYAPP_SIMPLE_STRING'
        ) == 'foo'
