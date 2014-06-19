#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cow.testing import CowTestCase
from tornado.httpclient import AsyncHTTPClient

from gaas.config import Config
from gaas.server import GaasServer
from gaas.models.repository import Repository


class TestCase(CowTestCase):
    def drop_collection(self, document):
        document.objects.delete(self.stop)
        self.wait()

    def setUp(self):
        super(TestCase, self).setUp()

        self.drop_collection(Repository)

    # def tearDown(self):
        # super(TestCase, self).tearDown()

    def get_config(self):
        return dict(
            MONGO_DATABASES={
                'default': {
                    'host': 'localhost',
                    'port': 4445,
                    'database': 'gaas-test',
                }
            },
            GIT_ROOT='/tmp/gaas_test/gitroot'
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
