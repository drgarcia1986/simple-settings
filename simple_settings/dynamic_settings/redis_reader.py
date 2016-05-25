# -*- coding: utf-8 -*-
import six
from redis import StrictRedis


class Reader(object):
    """
    Redis settings Reader
    A simple redis getter
    """
    _default_conf = {'host': 'localhost', 'port': 6379}

    def __init__(self, conf):
        self._default_conf.update(conf)

        self.redis = StrictRedis(
            host=self._default_conf['host'],
            port=self._default_conf['port']
        )

    def get(self, key):
        result = self.redis.get(key)
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')
        return result
