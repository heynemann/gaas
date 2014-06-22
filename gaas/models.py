#!/usr/bin/python
# -*- coding: utf-8 -*-


class Repository(object):
    def __init__(self, id, name, uuid, created_at):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.created_at = created_at
