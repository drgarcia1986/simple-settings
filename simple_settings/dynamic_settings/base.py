# -*- coding: utf-8 -*-
import re
from copy import deepcopy

import jsonpickle


class BaseReader(object):
    """
    Base class for dynamic readers
    """
    _default_conf = {}

    def __init__(self, conf):
        self.conf = deepcopy(self._default_conf)
        self.conf.update(conf)
        self.key_pattern = self.conf.get('pattern')
        self.auto_casting = self.conf.get('auto_casting')

    def get(self, key):
        if not self._is_valid_key(key):
            return
        result = self._get(key)
        if self.auto_casting:
            result = jsonpickle.decode(result)
        return result

    def set(self, key, value):
        if not self._is_valid_key(key):
            return
        if self.auto_casting:
            value = jsonpickle.encode(value)
        self._set(key, value)

    def _is_valid_key(self, key):
        if not self.key_pattern:
            return True
        return bool(re.match(self.key_pattern, key))
