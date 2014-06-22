#!/usr/bin/python
# -*- coding: utf-8 -*-

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
