#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import exists
import shutil

from preggy import expect
from tornado.testing import gen_test

from gaas.models.repository import Repository
from tests import TestCase
from tests.fixtures import RepositoryFactory


class CreateRepositoryHandlerTestCase(TestCase):
    @gen_test
    def test_create_repository(self):
        shutil.rmtree(self.server.config.GIT_ROOT)

        repo_name = 'repository_handler_test_1'
        response = self.fetch(
            '/repo/new',
            method='POST',
            body='name=%s' % repo_name
        )
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('OK')

        Repository.objects.get(name=repo_name, callback=self.stop)
        repo = self.wait()
        expect(repo).not_to_be_null()

        expect(response.headers).to_include('X-REPOSITORY-ID')
        expect(response.headers['X-REPOSITORY-ID']).to_equal(str(repo.uuid))

        path = '/tmp/gaas_test/gitroot/%s-%s/.git/' % (
            repo_name[:10],
            response.headers['X-REPOSITORY-ID']
        )
        expect(exists(path)).to_be_true()

    @gen_test
    def test_create_repository_already_exists(self):
        repo = yield RepositoryFactory.create()
        response = self.fetch(
            '/repo/new',
            method='POST',
            body='name=%s' % repo.name
        )
        expect(response.code).to_equal(409)
        expect(response.reason).to_be_like('Repository already exists')
