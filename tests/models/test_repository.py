#!/usr/bin/python
# -*- coding: utf-8 -*-


from preggy import expect
from tornado.testing import gen_test

from tests import TestCase
from tests.fixtures import RepositoryFactory


class RepositoryTestCase(TestCase):
    @gen_test
    def test_can_create_repository(self):
        repo = yield RepositoryFactory.create()

        expect(repo._id).not_to_be_null()
        expect(repo.name).to_include('repository_')
