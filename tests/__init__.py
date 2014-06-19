#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cow.testing import CowTestCase
from tornado.httpclient import AsyncHTTPClient
import tornado.gen as gen

from gaas.config import Config
from gaas.server import GaasServer


class TestCase(CowTestCase):
    @gen.coroutine
    def drop_collection(self, document):
        yield document.objects.delete()

    #def setUp(self):
        #super(ApiTestCase, self).setUp()

    #def tearDown(self):
        #super(ApiTestCase, self).tearDown()

    def get_config(self):
        return dict(
        )

    def get_server(self):
        cfg = Config(**self.get_config())
        debug = os.environ.get('DEBUG_TESTS', 'False').lower() == 'true'

        self.server = GaasServer(config=cfg, debug=debug)
        return self.server

    def get_app(self):
        app = super(TestCase, self).get_app()
        app.http_client = AsyncHTTPClient(self.io_loop)

        return app
