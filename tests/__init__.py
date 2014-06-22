#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from cow.testing import CowTestCase
from tornado.httpclient import AsyncHTTPClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from gaas.config import Config
from gaas.server import GaasServer
from gaas.storage.sqlalchemy import SqlAlchemyStorage
from tests.fixtures import SaRepositoryFactory


autoflush = True
engine = create_engine(
    "mysql+mysqldb://root@localhost:3306/test_gaas",
    convert_unicode=True,
    pool_size=1,
    max_overflow=0,
    echo=False
)
maker = sessionmaker(bind=engine, autoflush=autoflush)
db = scoped_session(maker)


class TestCase(CowTestCase):
    def drop_collection(self, document):
        document.objects.delete(self.stop)
        self.wait()

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


class SqlAlchemyStorageTestCase(TestCase):
    def get_server(self):
        cfg = Config(**self.get_config())
        debug = os.environ.get('DEBUG_TESTS', 'False').lower() == 'true'
        storage = SqlAlchemyStorage(None, None, cfg, self.io_loop)
        self.server = GaasServer(config=cfg, debug=debug, storage=storage)
        storage.server = self.server
        return self.server

    def get_app(self):
        app = super(TestCase, self).get_app()
        app.http_client = AsyncHTTPClient(self.io_loop)
        self.server.storage.application = app
        self.server.storage.initialize()

        return app

    def get_config(self):
        return dict(
            SQLALCHEMY_CONNECTION_STRING='mysql+mysqldb://root@localhost:3306/test_gaas',
            SQLALCHEMY_AUTO_FLUSH=True,
            SQLALCHEMY_POOL_SIZE=1,
            SQLALCHEMY_POOL_MAX_OVERFLOW=0,
            GIT_ROOT='/tmp/gaas_test/gitroot',
        )

    def setUp(self):
        super(TestCase, self).setUp()
        self.server.application.storage.session = db
        SaRepositoryFactory.FACTORY_SESSION = db
        self.server.application.storage.connect()

    @property
    def db(self):
        return db

    def tearDown(self):
        super(TestCase, self).tearDown()
        self.server.application.storage.disconnect(error=True, close_connection=False)
