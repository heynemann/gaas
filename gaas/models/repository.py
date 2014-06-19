#!/usr/bin/python
# -*- coding: utf-8 -*-

from uuid import uuid4

from motorengine import (
    Document, DateTimeField,
    StringField, UUIDField
)


class Repository(Document):
    date = DateTimeField(required=True, auto_now_on_insert=True)
    name = StringField(required=True)
    uuid = UUIDField(required=True, default=uuid4)
