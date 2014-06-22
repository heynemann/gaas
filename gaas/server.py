#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import exists, abspath, join
import datetime

from cow.server import Server
from cow.plugins.motorengine_plugin import MotorEnginePlugin
from tornado.httpclient import AsyncHTTPClient
from gaas.git import RPCHandler, FileHandler, InfoRefsHandler
from gittornado.util import get_date_header

from gaas import __version__
from gaas import git
from gaas.utils import get_class
from gaas.handlers import BaseHandler
from gaas.handlers.repository import (
    CreateRepositoryHandler
)


cache_forever = lambda: [('Expires', get_date_header(datetime.datetime.now() + datetime.timedelta(days=365))),
                 ('Pragma', 'no-cache'),
                 ('Cache-Control', 'public, max-age=31556926')]

dont_cache = lambda: [('Expires', 'Fri, 01 Jan 1980 00:00:00 GMT'),
              ('Pragma', 'no-cache'),
              ('Cache-Control', 'no-cache, max-age=0, must-revalidate')]


def main():
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    GaasServer.run()
    # after many bizarre tests this should be the way to go:
    # https://moocode.com/posts/6-code-your-own-multi-user-private-git-server-in-5-minutes


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
        self.application.storage_module = get_class(self.config.STORAGE)
        self.application.storage = self.application.storage_module(self, self.application, self.config, io_loop)
        self.application.storage.define_config(self.config)
        self.config.reload()
        self.application.storage.initialize()

    def before_end(self, io_loop):
        self.application.storage.destruct()

if __name__ == '__main__':
    main()
