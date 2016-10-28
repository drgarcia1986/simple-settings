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

    def _get(self, key):
        try:
            return self.session.kv[key]
        except KeyError:
            return None

    def _set(self, key, value):
        self.session.kv.set(key, value)

    def _qualified_key(self, key):
        """
        Prepends the configured prefix to the key (if applicable).

        For Consul we also lstrip any '/' chars from the prefixed key.

        :param key: The unprefixed key.
        :return: The key with any configured prefix prepended.
        """
        fq_key = super(Reader, self)._qualified_key(key)
        return fq_key.lstrip('/')
