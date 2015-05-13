# -*- coding: utf-8 -*-
from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from simple_settings import settings


class ConfigHandler(RequestHandler):
    def get(self):
        self.finish({
            'example_foo': settings.EXAMPLE_FOO,
            'example_bar': settings.EXAMPLE_BAR
        })


if __name__ == '__main__':
    app = Application(
        handlers=[(r'/', ConfigHandler)],
        debug=settings.DEBUG
    )
    server = HTTPServer(app)
    server.listen(settings.PORT)
    IOLoop.instance().start()
