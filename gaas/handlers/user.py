#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

from tornado import gen

from gaas.handlers import BaseHandler


class CreateUserHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        name = self.get_argument('name')

        user = yield self.storage.get_user_by_name(name)

        if user is not None:
            self.set_status(409, 'User already exists')
            self.finish()
            return

        user = yield self.storage.create_user(
            name=name
        )

        self.set_header('X-USER-ID', user.slug)
        self.write('OK')
        self.finish()


class AddUserKeyHandler(BaseHandler):
    @gen.coroutine
    def post(self, user_slug):
        user = yield self.storage.get_user_by_slug(user_slug)

        if user is None:
            self.set_status(404, 'User not found')
            self.finish()
            return

        public_key = self.get_argument('key')

        if not public_key:
            self.set_status(404, 'Invalid public key')
            self.finish()
            return

        yield self.storage.add_user_key(
            user=user,
            key=public_key
        )

        self.write('OK')
        self.finish()
