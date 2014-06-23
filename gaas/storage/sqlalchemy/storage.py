#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import logging
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from alembic.config import Config
from alembic import command
from tornado import gen
from slugify import slugify

from gaas.storage.base import BaseStorage
from gaas.storage.sqlalchemy.models import Repository, User, Key

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

        config.define(
            'SQLALCHEMY_COMMIT_ON_DISCONNECT',
            True,
            'Whether SqlAlchemy should commit when disconnecting.',
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
        elif self.config.SQLALCHEMY_COMMIT_ON_DISCONNECT:
            self.session.commit()

        if close_connection:
            self.session.close()

    def destruct(self):
        pass

    def migrate(self):
        alembic_cfg = Config(self.config.ALEMBIC_CONFIGURATION_PATH)
        command.upgrade(alembic_cfg, "head")

    @gen.coroutine
    def get_repository_by_name(self, name):
        repository = self.session.query(Repository).filter(Repository.name == name).first()
        raise gen.Return(repository)

    @gen.coroutine
    def create_repository(self, name):
        repository = Repository(
            name=name,
            slug=slugify(name)
        )
        self.session.add(repository)
        self.session.flush()
        raise gen.Return(repository)

    @gen.coroutine
    def get_user_by_name(self, name):
        user = self.session.query(User).filter(User.name == name).first()
        raise gen.Return(user)

    @gen.coroutine
    def get_user_by_slug(self, slug):
        user = self.session.query(User).filter(User.slug == slug).first()
        raise gen.Return(user)

    @gen.coroutine
    def add_user_key(self, user, key):
        public_key = key.split(' ')
        if len(public_key) == 1:
            key = public_key[0]
        else:
            key = public_key[1]

        public_key_hash = hashlib.sha512(key).hexdigest()

        key = Key(
            user=user,
            public_key=key,
            public_key_hash=public_key_hash
        )

        self.session.add(key)
        self.session.flush()
        raise gen.Return(key)

    @gen.coroutine
    def create_user(self, name):
        user = User(
            name=name,
            slug=slugify(name)
        )
        self.session.add(user)
        self.session.flush()
        raise gen.Return(user)
