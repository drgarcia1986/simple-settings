# -*- coding: utf-8 -*-
import consulate


class Reader(object):
    """
    Consul settings Reader

    A simple consul getter using consulate library.
    """
    _default_conf = {
        'host': consulate.DEFAULT_HOST,
        'port': consulate.DEFAULT_PORT,
        'scheme': consulate.DEFAULT_SCHEME
    }

    def __init__(self, conf):
        self._default_conf.update(conf)
        self.session = consulate.Consul(
            host=self._default_conf['host'],
            port=self._default_conf['port'],
            datacenter=self._default_conf.get('datacenter'),
            token=self._default_conf.get('token'),
            scheme=self._default_conf['scheme']
        )

    def get(self, key):
        try:
            return self.session.kv[key]
        except KeyError:
            return None  # Just to be explicit.
