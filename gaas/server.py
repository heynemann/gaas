#!/usr/bin/python
# -*- coding: utf-8 -*-

from cow.server import Server
from cow.plugins.motorengine_plugin import MotorEnginePlugin
from tornado.httpclient import AsyncHTTPClient

from gaas import __version__
from gaas.handlers import BaseHandler
from gaas.handlers.repository import (
    CreateRepositoryHandler
)


def main():
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    GaasServer.run()


class VersionHandler(BaseHandler):
    def get(self):
        self.write(__version__)


class GaasServer(Server):
    def __init__(self, debug=None, *args, **kw):
        super(GaasServer, self).__init__(*args, **kw)

        self.force_debug = debug

    def initialize_app(self, *args, **kw):
        super(GaasServer, self).initialize_app(*args, **kw)

        if self.force_debug is not None:
            self.debug = self.force_debug

    def get_handlers(self):
        handlers = [
            ('/version/?', VersionHandler),
            ('/repo/new/?', CreateRepositoryHandler),
        ]

        return tuple(handlers)

    def get_plugins(self):
        return [
            MotorEnginePlugin,
        ]

    def after_start(self, io_loop):
        pass

    def before_end(self, io_loop):
        pass

if __name__ == '__main__':
    main()
