# -*- coding: utf-8 -*-
from .base import BaseReader

try:
    from redis import StrictRedis
    import six
except ImportError:  # pragma: no cover
    raise ImportError(
        'To use "redis" dynamic settings reader\n'
        'you need to install simple-settings with redis dependency:\n'
        'pip install simple-settings[redis] or pip install redis'
    )


class Reader(BaseReader):
    """
    Redis settings Reader
    A simple redis getter
    """
    _default_conf = {'host': 'localhost', 'port': 6379}

    def __init__(self, conf):
        super(Reader, self).__init__(conf)

        self.redis = StrictRedis(
            host=self.conf['host'],
            port=self.conf['port']
        )

    def _get(self, key):
        result = self.redis.get(key)
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')
        return result

    def _set(self, key, value):
        self.redis.set(key, value)
