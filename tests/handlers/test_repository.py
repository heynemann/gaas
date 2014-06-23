#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import exists
import shutil

from preggy import expect
from tornado.testing import gen_test

from tests import SqlAlchemyStorageTestCase
from tests.fixtures import SaRepositoryFactory


class CreateRepositoryHandlerTestCase(SqlAlchemyStorageTestCase):
    @gen_test
    def test_create_repository(self):
        if exists(self.server.config.GIT_ROOT):
            shutil.rmtree(self.server.config.GIT_ROOT)

        repo_name = 'repository handler test 1'
        response = self.fetch(
            '/repo/new',
            method='POST',
            body='name=%s' % repo_name
        )
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('OK')

        repo = yield self.storage.get_repository_by_name(repo_name)
        expect(repo).not_to_be_null()

        expect(response.headers).to_include('X-REPOSITORY-ID')
        expect(response.headers['X-REPOSITORY-ID']).to_equal(str(repo.slug))

        path = '%s/%s' % (
            self.server.config.GIT_ROOT.rstrip('/'),
            response.headers['X-REPOSITORY-ID']
        )
        expect(exists(path)).to_be_true()

    from nose_focus import focus
    @focus
    @gen_test
    def test_create_repository_already_exists(self):
        repo = SaRepositoryFactory.create()
        response = self.fetch(
            '/repo/new',
            method='POST',
            body='name=%s' % repo.name
        )
        expect(response.code).to_equal(409)
        expect(response.reason).to_be_like('Repository already exists')
