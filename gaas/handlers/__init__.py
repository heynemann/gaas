#!/usr/bin/python
# -*- coding: utf-8 -*-

from ujson import dumps
from tornado.web import RequestHandler

from gaas import __version__


class BaseHandler(RequestHandler):
    def initialize(self, *args, **kw):
        super(BaseHandler, self).initialize(*args, **kw)
        self.application.storage.connect()

    #def log_exception(self, typ, value, tb):
        #for handler in self.application.error_handlers:
            #handler.handle_exception(
                #typ, value, tb, extra={
                    #'url': self.request.full_url(),
                    #'ip': self.request.remote_ip,
                    #'holmes-version': __version__
                #}
            #)

        #super(BaseHandler, self).log_exception(typ, value, tb)

    def on_finish(self):
        self.storage.disconnect(self.get_status() > 399)

    def write_json(self, obj):
        self.set_header("Content-Type", "application/json")
        self.write(dumps(obj))

    @property
    def storage(self):
        return self.application.storage

    @property
    def config(self):
        return self.application.config
