#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado import gen

from gaas import git
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

        name = "%s-%s" % (repo.name[:10], str(repo.uuid))
        git.create_git_repo(name, self.config.GIT_ROOT)

        self.set_header('X-REPOSITORY-ID', str(repo.uuid))
        self.write('OK')
        self.finish()
