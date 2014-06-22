#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import exists
import shutil

from preggy import expect
from tornado.testing import gen_test

from tests import SqlAlchemyStorageTestCase
from tests.fixtures import SaUserFactory


class CreateUserHandlerTestCase(SqlAlchemyStorageTestCase):
    @gen_test
    def test_create_user(self):
        if exists(self.server.config.GIT_ROOT):
            shutil.rmtree(self.server.config.GIT_ROOT)

        user_name = 'user handler test 1'
        response = self.fetch(
            '/user/new',
            method='POST',
            body='name=%s' % user_name
        )
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('OK')

        user = yield self.storage.get_user_by_name(user_name)
        expect(user).not_to_be_null()

        expect(response.headers).to_include('X-USER-ID')
        expect(response.headers['X-USER-ID']).to_equal(str(user.slug))

    @gen_test
    def test_create_user_already_exists(self):
        user = SaUserFactory.create()
        response = self.fetch(
            '/user/new',
            method='POST',
            body='name=%s' % user.name
        )
        expect(response.code).to_equal(409)
        expect(response.reason).to_be_like('User already exists')
