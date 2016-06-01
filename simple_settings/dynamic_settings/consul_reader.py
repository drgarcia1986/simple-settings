# -*- coding: utf-8 -*-
import six
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
        self.session = consulate.Consul(host=self._default_conf['host'], port=self._default_conf['port'],
                                        datacenter=self._default_conf.get('datacenter'),
                                        token=self._default_conf.get('token'), scheme=self._default_conf['scheme'])

    def get(self, key):
        try:
            result = self.session.kv[key]
        except KeyError:
            result = None
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')
        return result
