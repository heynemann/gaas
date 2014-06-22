#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from alembic.config import Config
from alembic import command

from gaas.storage.base import BaseStorage

logger = logging.getLogger(__file__)


class SqlAlchemyStorage(BaseStorage):
    def define_config(self, config):
        config.define(
            'SQLALCHEMY_CONNECTION_STRING',
            'mysql+mysqldb://root@localhost:3306/gaas',
            'Connection string to the database SqlAlchemy must connect to.',
            'Storage'
        )

        config.define(
            'SQLALCHEMY_POOL_SIZE',
            20,
            'Number of connection to keep in the pool for SqlAlchemy.',
            'Storage'
        )

        config.define(
            'SQLALCHEMY_POOL_MAX_OVERFLOW',
            10,
            'Number of connection to use as max overflow pool for SqlAlchemy.',
            'Storage'
        )

        config.define(
            'SQLALCHEMY_AUTO_FLUSH',
            False,
            'Whether SqlAlchemy should auto-flush every transaction.',
            'Storage'
        )

        local_alembic_path = abspath(join(dirname(__file__), './alembic.ini'))
        config.define(
            'ALEMBIC_CONFIGURATION_PATH',
            local_alembic_path,
            'Path to the alembic configuration file to run migrations.',
            'Storage'
        )

    def initialize(self):
        autoflush = self.config.SQLALCHEMY_AUTO_FLUSH
        connstr = self.config.SQLALCHEMY_CONNECTION_STRING
        engine = create_engine(
            connstr,
            convert_unicode=True,
            pool_size=self.config.SQLALCHEMY_POOL_SIZE,
            max_overflow=self.config.SQLALCHEMY_POOL_MAX_OVERFLOW,
            echo=self.server.debug
        )

        logger.info("Connecting to \"%s\" using SQLAlchemy" % connstr)

        self.sqlalchemy_db_maker = sessionmaker(
            bind=engine,
            autoflush=autoflush
        )
        self.get_sqlalchemy_session = \
            lambda: scoped_session(self.sqlalchemy_db_maker)

    def connect(self):
        if getattr(self, 'session', None) is None:
            self.session = self.get_sqlalchemy_session()

    def disconnect(self, error, close_connection=True):
        if not self.session:
            return

        if error:
            self.session.rollback()
        else:
            self.session.commit()

        if close_connection:
            self.session.close()
        self.session = None

    def destruct(self):
        pass

    def migrate(self):
        alembic_cfg = Config(self.config.ALEMBIC_CONFIGURATION_PATH)
        command.upgrade(alembic_cfg, "head")
