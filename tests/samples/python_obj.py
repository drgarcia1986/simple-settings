# -*- coding: utf-8 -*-


class MyConfig(object):
    START_URLS = ['https://www.google.com']
    AUTO_CONNECT = True


def config_invalid():
    START_URLS = ['https://www.google.com']
    AUTO_CONNECT = True
