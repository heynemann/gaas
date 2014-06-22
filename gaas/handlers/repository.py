#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado import gen

from gaas import git
from gaas.handlers import BaseHandler


class CreateRepositoryHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        name = self.get_argument('name')

        repo = yield self.storage.get_repository_by_name(name)

        if repo is not None:
            self.set_status(409, 'Repository already exists')
            self.finish()
            return

        repo = yield self.storage.create_repository(
            name=name
        )

        git.create_git_repo(self.config.GIT_ROOT, repo.slug, bare=True)

        self.set_header('X-REPOSITORY-ID', repo.slug)
        self.write('OK')
        self.finish()
