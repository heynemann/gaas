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
