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


class AddUserKeyHandlerTestCase(SqlAlchemyStorageTestCase):
    @gen_test
    def test_add_user_key(self):
        user = SaUserFactory.create()
        key = """ssh-rsa DAAAB3NzaC1yc2EAAAADAQABAAABAQD5eYo2ZM8Inuf73WqA3C8HCPjb1DUWLs4z2x+eCY3VHc7oZZmVguB/kAGxUmIpxvMKtNeOicHIfUvJ6UIibl2vagFn0+t8KooUovbPugxFSEeuYPKcqhA5U3hlAGbYa2HS5Z+2pImLidQuCnv07vO7cQFshEndsX11ff4ZjrpvI+LoidzZkxeOwGkMTrkmMNrvT4u26OBQGPHJU0JVq3e4X1FjrdSQ2lJHZ5qxdyZn84pypyPctc2WaNeHKV0h4UeqRK7VLCjpkrNXpZlFj0JO3Yetac2bkl6qpR+FuUPUdxeTb2QmdHFi6MN1yfX+YBSTxMWniC/gQDRQ8PYYTAvV heynemann@someserver"""

        response = self.fetch(
            '/users/%s/add-key' % user.slug,
            method='POST',
            body='key=%s' % key
        )
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('OK')

        user = yield self.storage.get_user_by_name(user.name)
        expect(user).not_to_be_null()
        expect(user.keys).to_length(1)

        expect(user.keys[0].public_key).to_equal(key.split(' ')[1])
