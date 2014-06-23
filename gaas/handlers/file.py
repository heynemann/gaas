#!/usr/bin/python
# -*- coding: utf-8 -*-

import shlex

from tornado import gen
import tornado.process

from gaas import git
from gaas.handlers import BaseHandler


STREAM = tornado.process.Subprocess.STREAM


@gen.coroutine
def call_subprocess(cmd, cwd=None):
    """
    Wrapper around subprocess call using Tornado's Subprocess class.
    """
    stdin = tornado.process.subprocess.PIPE

    sub_process = tornado.process.Subprocess(
        cmd, stdin=stdin, stdout=STREAM, stderr=STREAM, cwd=cwd
    )

    result, error = yield [
        gen.Task(sub_process.stdout.read_until_close),
        gen.Task(sub_process.stderr.read_until_close)
    ]

    raise gen.Return((result, error))


class ShowFileHandler(BaseHandler):
    @gen.coroutine
    def get(self, repo, branch, path):
        cwd = '%s/%s' % (
            self.config.GIT_ROOT,
            repo,
        )
        cmd = '/usr/bin/git show %s:%s' % (
            branch,
            path
        )

        result, error = yield call_subprocess(shlex.split(cmd), cwd=cwd)

        self.write(result)
        self.finish()
