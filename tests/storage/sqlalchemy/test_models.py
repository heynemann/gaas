#!/usr/bin/python
# -*- coding: utf-8 -*-

from preggy import expect

from gaas.storage.sqlalchemy.models import Repository, User, Key
from tests import SqlAlchemyStorageTestCase
from tests.fixtures import SaRepositoryFactory, SaUserFactory, SaKeyFactory


class RepositoryModelTestCase(SqlAlchemyStorageTestCase):
    def test_can_create_repository(self):
        repo = SaRepositoryFactory.create()
        expect(repo.id).to_be_greater_than(0)

        repository = self.db.query(Repository).filter(Repository.name == repo.name).one()
        expect(repository).not_to_be_null()
        expect(repository.id).to_equal(repo.id)
        expect(repository.name).to_equal(repo.name)
        expect(repository.slug).to_equal(repo.slug)


class UserModelTestCase(SqlAlchemyStorageTestCase):
    def test_can_create_user(self):
        user = SaUserFactory.create()
        expect(user.id).to_be_greater_than(0)

        loaded = self.db.query(User).filter(User.name == user.name).one()
        expect(loaded).not_to_be_null()
        expect(loaded.id).to_equal(user.id)
        expect(loaded.name).to_equal(user.name)
        expect(loaded.slug).to_equal(user.slug)


class KeysModelTestCase(SqlAlchemyStorageTestCase):
    def test_can_create_key(self):
        user = SaUserFactory.create()

        key = SaKeyFactory.create(user=user)

        loaded = self.db.query(Key).filter(Key.id == key.id).one()
        expect(loaded).not_to_be_null()
        expect(loaded.id).to_equal(key.id)
        expect(loaded.public_key).to_equal(key.public_key)

        self.db.refresh(user)
        expect(user.keys).to_length(1)
        expect(user.keys[0].id).to_equal(key.id)
