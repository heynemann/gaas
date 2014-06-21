#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os.path import abspath, join, exists, dirname

import pygit2
import urlparse
import re
import os.path
import datetime

import tornado.web

from gittornado.iowrapper import ProcessWrapper, FileWrapper
from gittornado.util import get_date_header

import logging
logger = logging.getLogger(__name__)

cache_forever = lambda: [('Expires', get_date_header(datetime.datetime.now() + datetime.timedelta(days=365))),
                 ('Pragma', 'no-cache'),
                 ('Cache-Control', 'public, max-age=31556926')]

dont_cache = lambda: [('Expires', 'Fri, 01 Jan 1980 00:00:00 GMT'),
              ('Pragma', 'no-cache'),
              ('Cache-Control', 'no-cache, max-age=0, must-revalidate')]

def create_git_repo(git_root, name, bare=False):
    path = abspath(join(
        git_root,
        name
    ))

    if not exists(dirname(path)):
        os.makedirs(dirname(path))

    return pygit2.init_repository(path, bare=bare)


def clone(repo_url, repo_path, ref='refs/heads/master'):
    repo = pygit2.clone_repository(repo_url, repo_path)
    repo.checkout(ref)
    return repo


class BaseHandler(tornado.web.RequestHandler):
    auth = None
    auth_failed = None
    gitlookup = None
    gitcommand = None

    public_readble = True
    public_writable = False

    def initialize(self, **kwargs):
        for name, value in kwargs.items():
            if hasattr(self, name) and getattr(self, name) is None:
                setattr(self, name, value)

        # set defaults
        if self.gitcommand is None:
            self.gitcommand = 'git'

    def get_gitdir(self):
        """Determine the git repository for this request"""
        if self.gitlookup is None:
            raise tornado.web.HTTPError(500, 'no git lookup configured')

        gitdir = self.gitlookup(self.request)
        if gitdir is None:
            raise tornado.web.HTTPError(404, 'unable to find repository')
        logger.debug("Accessing git at: %s", gitdir)

        return gitdir

    def check_auth(self):
        """Check authentication/authorization of client"""
        # access permissions
        if self.auth is not None:
            return self.auth(self.request)

        return self.public_readble, self.public_writable

    def enforce_perms(self, rpc):
        read, write = self.check_auth()

        if rpc in ['git-receive-pack', 'receive-pack']:
            if not write:
                if self.auth_failed:
                    self.auth_failed(self.request)
                    self.request.finish()
                    return False
                else:
                    raise tornado.web.HTTPError(403, 'You are not allowed to perform this action')

        elif rpc in ['git-upload-pack', 'upload-pack']:
            if not read:
                if self.auth_failed:
                    self.auth_failed(self.request)
                    self.request.finish()
                    return False
                else:
                    raise tornado.web.HTTPError(403, 'You are not allowed to perform this action')

        else:
            raise tornado.web.HTTPError(400, 'Unknown RPC command')

        return True

class RPCHandler(BaseHandler):
    """Request handler for RPC calls

    Use this handler to handle example.git/git-upload-pack and example.git/git-receive-pack URLs"""
    @tornado.web.asynchronous
    def post(self):
        gitdir = self.get_gitdir()

        # get RPC command
        pathlets = self.request.path.strip('/').split('/')
        rpc = pathlets[-1]
        if not self.enforce_perms(rpc):
            return
        rpc = rpc[4:]

        ProcessWrapper(self.request, [self.gitcommand, rpc, '--stateless-rpc', gitdir],
                       {'Content-Type': 'application/x-git-%s-result' % rpc})

class InfoRefsHandler(BaseHandler):
    """Request handler for info/refs

    Use this handler to handle example.git/info/refs?service= URLs"""

    @tornado.web.asynchronous
    def get(self):
        gitdir = self.get_gitdir()

        logger.debug("Query string: %r", self.request.query)
        rpc = urlparse.parse_qs(self.request.query).get('service', [''])[0]

        read, write = self.check_auth()
        if not read:
            if self.auth_failed:
                self.auth_failed(self.request)
                self.request.finish()
                return
            else:
                raise tornado.web.HTTPError(403, 'You are not allowed to perform this action')

        if not rpc:
            # this appears to be a dumb client. send the file
            logger.debug("Dumb client detected")
            FileWrapper(self.request, os.path.join(gitdir, 'info', 'refs'), dict(dont_cache() + [('Content-Type', 'text/plain; charset=utf-8')]))
            return

        rpc = rpc[4:]

        prelude = '# service=git-' + rpc
        prelude = str(hex(len(prelude) + 4)[2:].rjust(4, '0')) + prelude
        prelude += '0000' # packet flush

        ProcessWrapper(self.request, [self.gitcommand, rpc, '--stateless-rpc', '--advertise-refs', gitdir],
                       {'Content-Type': 'application/x-git-%s-advertisement' % rpc,
                        'Expires': 'Fri, 01 Jan 1980 00:00:00 GMT',
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache, max-age=0, must-revalidate'}, prelude)

file_headers = {
    re.compile('.*(/HEAD)$'):                                   lambda: dict(dont_cache() + [('Content-Type', 'text/plain')]),
    re.compile('.*(/objects/info/alternates)$'):                lambda: dict(dont_cache() + [('Content-Type', 'text/plain')]),
    re.compile('.*(/objects/info/http-alternates)$'):           lambda: dict(dont_cache() + [('Content-Type', 'text/plain')]),
    re.compile('.*(/objects/info/packs)$'):                     lambda: dict(dont_cache() + [('Content-Type', 'text/plain; charset=utf-8')]),
    re.compile('.*(/objects/info/[^/]+)$'):                     lambda: dict(dont_cache() + [('Content-Type', 'text/plain')]),
    re.compile('.*(/objects/[0-9a-f]{2}/[0-9a-f]{38})$'):       lambda: dict(cache_forever() + [('Content-Type', 'application/x-git-loose-object')]),
    re.compile('.*(/objects/pack/pack-[0-9a-f]{40}\\.pack)$'):  lambda: dict(cache_forever() + [('Content-Type', 'application/x-git-packed-objects')]),
    re.compile('.*(/objects/pack/pack-[0-9a-f]{40}\\.idx)$'):   lambda: dict(cache_forever() + [('Content-Type', 'application/x-git-packed-objects-toc')]),
}

class FileHandler(BaseHandler):
    """Request handler for static files"""
    @tornado.web.asynchronous
    def get(self):
        gitdir = self.get_gitdir()

        read, write = self.check_auth()
        if not read:
            if self.auth_failed:
                self.auth_failed(self.request)
                self.request.finish()
                return
            else:
                raise tornado.web.HTTPError(403, 'You are not allowed to perform this action')

        # determine the headers for this file
        filename, headers = None, None
        for matcher, get_headers in file_headers.items():
            m = matcher.match(self.request.path)
            if m:
                filename = m.group(1)
                headers = get_headers()
                break

        logger.debug("Found %r with headers %r", filename, headers)

        # did we find anything?
        if not filename:
            raise tornado.web.HTTPError(404, 'File not Found')

        # expand filename
        filename = os.path.abspath(os.path.join(gitdir, filename.lstrip('/')))
        if not filename.startswith(os.path.abspath(gitdir)): # yes, the matches are strict and don't allow directory traversal, but better safe than sorry
            raise tornado.web.HTTPError(404, 'Trying to access file outside of git repository')

        logger.debug('Serving file %s', filename)

        FileWrapper(self.request, filename, headers)
