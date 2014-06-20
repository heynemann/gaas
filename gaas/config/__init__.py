#!/usr/bin/python
# -*- coding: utf-8 -*-

from derpconf.config import Config  # NOQA

Config.define('MONGO_DATABASES', {
    'default': {
        'host': 'localhost',
        'port': 4445,
        'database': 'gaas',
    }
}, 'MongoDB Database connection.', 'Database')

Config.define(
    'GIT_ROOT',
    '/tmp/gaas/gitroot',
    'Root folder to store git repositories.',
    'Git'
)

#Config.define(
    #'GITOLITE_ROOT',
    #'/tmp/gaas/gitolite_admin',
    #'Directory to clone gitolite admin repository to.',
    #'Gitolite'
#)

#Config.define(
    #'GITOLITE_URL',
    #'ssh://local.gaas.com/gitolite-admin.git',
    #'Url to clone gitolite admin repository from.',
    #'Gitolite'
#)
