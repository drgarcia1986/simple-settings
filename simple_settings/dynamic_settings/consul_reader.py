# -*- coding: utf-8 -*-
from .base import BaseReader

try:
    import consulate
except ImportError:  # pragma: no cover
    raise ImportError(
        'To use "consul" dynamic settings reader\n'
        'you need to install simple-settings with consulate dependency:\n'
        'pip install simple-settings[consul] or pip install consulate'
    )


class Reader(BaseReader):
    """
    Consul settings Reader

    A simple consul getter using consulate library.
    """
    _default_conf = {
        'host': consulate.DEFAULT_HOST,
        'port': consulate.DEFAULT_PORT,
        'scheme': consulate.DEFAULT_SCHEME,
        'prefix': ''
    }

    def __init__(self, conf):
        super(Reader, self).__init__(conf)

        self.session = consulate.Consul(
            host=self.conf['host'],
            port=self.conf['port'],
            datacenter=self.conf.get('datacenter'),
            token=self.conf.get('token'),
            scheme=self.conf['scheme']
        )

    def _qualified_key(self, key):
        """
        Prepends the prefix to the key (if applicable).

        :param key: The unprefixed key.
        :return: The qualifeid key.
        """
        if self.conf.get('prefix') is None:
            return key
        else:
            return '{}{}'.format(self.conf['prefix'], key)

    def _get(self, key):
        try:
            return self.session.kv[self._qualified_key(key)]
        except KeyError:
            return None

    def _set(self, key, value):
        self.session.kv.set(self._qualified_key(key), value)
