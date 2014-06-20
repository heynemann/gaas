#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import exists, abspath, join

from cow.server import Server
from cow.plugins.motorengine_plugin import MotorEnginePlugin
from tornado.httpclient import AsyncHTTPClient
from gittornado import RPCHandler, InfoRefsHandler, FileHandler

from gaas import __version__
from gaas import git
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

    def auth(self, request):
        pathlets = request.path.strip('/').split('/')

        author = request.headers.get('Authorization', None)
        if author is None:
            return True, False

        if author.strip().lower()[:5] != 'basic':
            return True, False

        userpw_base64 = author.strip()[5:].strip()

        user, pw = userpw_base64.decode('base64').split(':', 1)

        #if accessfile.has_option('users', user):
            #if accessfile.get('users', user) == pw:
                #if accessfile.has_option('access', user):
                    #return True, pathlets[0] in accessfile.get('access', user).split(',')

        return True, True

    def gitlookup(self, request):
        pathlets = request.path.strip('/').split('/')

        path = abspath(join(self.config.GIT_ROOT, pathlets[0]))
        if not path.startswith(abspath(self.config.GIT_ROOT)):
            return None

        if exists(path):
            return path

    def auth_failed(self, request):
        msg = 'Authorization needed to access this repository'
        request.write('HTTP/1.1 401 Unauthorized\r\nContent-Type: text/plain\r\nContent-Length: %d\r\nWWW-Authenticate: Basic realm="%s"\r\n\r\n%s' % (
            len(msg), "localhost", msg))

    def get_handlers(self):
        conf = {
            'auth': self.auth,
            'gitlookup': self.gitlookup,
            'auth_failed': self.auth_failed
        }
        handlers = [
            ('/version/?', VersionHandler),
            ('/repo/new/?', CreateRepositoryHandler),
            ('/.*/git-.*', RPCHandler, conf),
            ('/.*/info/refs', InfoRefsHandler, conf),
            ('/.*/HEAD', FileHandler, conf),
            ('/.*/objects/.*', FileHandler, conf),
        ]

        return tuple(handlers)

    def get_plugins(self):
        return [
            MotorEnginePlugin,
        ]

    def after_start(self, io_loop):
        #if not exists(self.config.GITOLITE_ROOT):
            #git.clone(self.config.GITOLITE_URL, self.config.GITOLITE_ROOT)
        pass

    def before_end(self, io_loop):
        pass

if __name__ == '__main__':
    main()
