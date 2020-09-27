from .base import BaseReader

try:
    import six
    from pymemcache.client.base import Client
except ImportError:  # pragma: no cover
    raise ImportError(
        'To use "memcached" dynamic settings reader\n'
        'you need to install simple-settings with memcached dependency:\n'
        'pip install simple-settings[memcached] or pip install pymemcache'
    )


class Reader(BaseReader):
    """
    Memcached settings Reader

    A simple memcached getter using pymemcache library.
    """
    _default_conf = {
        'host': 'localhost',
        'port': 11211
    }

    def __init__(self, conf):
        super(Reader, self).__init__(conf)

        self.client = Client((self.conf['host'], self.conf['port']))

    def _get(self, key):
        result = self.client.get(key)
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')

        return result

    def _set(self, key, value):
        self.client.set(key, value, noreply=False)
