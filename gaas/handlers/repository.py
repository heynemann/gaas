#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os.path import abspath, join, exists, dirname

from tornado import gen
import pygit2

from gaas.handlers import BaseHandler
from gaas.models.repository import Repository


class CreateRepositoryHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        name = self.get_argument('name')

        repo = yield Repository.objects.get(name=name)
        if repo is not None:
            self.set_status(409, 'Repository already exists')
            self.finish()
            return

        repo = yield Repository.objects.create(
            name=name
        )

        self.create_git_repo(repo)

        self.set_header('X-REPOSITORY-ID', str(repo.uuid))
        self.write('OK')
        self.finish()

    def create_git_repo(self, repository):
        path = abspath(join(
            self.config.GIT_ROOT,
            "%s-%s" % (repository.name[:10], str(repository.uuid))
        ))

        if not exists(dirname(path)):
            os.makedirs(dirname(path))

        return pygit2.init_repository(path, False)
