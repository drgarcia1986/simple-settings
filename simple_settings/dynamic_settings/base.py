# -*- coding: utf-8 -*-
import re
from copy import deepcopy


class BaseReader(object):
    """
    Base class for dynamic readers
    """
    _default_conf = {}

    def __init__(self, conf):
        self.conf = deepcopy(self._default_conf)
        self.conf.update(conf)

    def get(self, key):
        if self._is_valid_key(key):
            return self._get(key)

    def _is_valid_key(self, key):
        pattern = self.conf.get('pattern')
        if not pattern:
            return True
        return bool(re.match(pattern, key))
