# -*- coding: utf-8 -*-
from copy import deepcopy

import six
from redis import StrictRedis


class Reader(object):

    _instance = None
    _default_conf = {'host': 'localhost', 'port': 6379}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Reader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._initialized = False

    def setup(self, conf):
        if self._initialized:
            return
        default_conf = deepcopy(self._default_conf)
        default_conf.update(conf)

        self.redis = StrictRedis(
            host=default_conf['host'], port=default_conf['port']
        )
        self._initialized = True

    def get(self, key):
        result = self.redis.get(key)
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')
        return result
