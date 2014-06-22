#!/usr/bin/python
# -*- coding: utf-8 -*-

from preggy import expect
from tornado.testing import gen_test

from tests import SqlAlchemyStorageTestCase
from tests.fixtures import SaRepositoryFactory, SaUserFactory


class StorageTestCase(SqlAlchemyStorageTestCase):
    @gen_test
    def test_can_get_repository_by_name(self):
        repo = SaRepositoryFactory.create()

        loaded = yield self.storage.get_repository_by_name(repo.name)

        expect(loaded.id).to_equal(repo.id)

    @gen_test
    def test_can_create_repository(self):
        name = "sqlalchemy storage test can create repository"
        slug = "sqlalchemy-storage-test-can-create-repository"
        repo = yield self.storage.create_repository(name)

        expect(repo.id).to_be_greater_than(0)
        expect(repo.name).to_equal(name)
        expect(repo.slug).to_equal(slug)

    @gen_test
    def test_can_get_user_by_name(self):
        user = SaUserFactory.create()

        loaded = yield self.storage.get_user_by_name(user.name)

        expect(loaded.id).to_equal(user.id)

    @gen_test
    def test_can_create_user(self):
        name = "sqlalchemy storage test can create user"
        slug = "sqlalchemy-storage-test-can-create-user"
        user = yield self.storage.create_user(name)

        expect(user.id).to_be_greater_than(0)
        expect(user.name).to_equal(name)
        expect(user.slug).to_equal(slug)
