#!/usr/bin/python
# -*- coding: utf-8 -*-


from cow.plugins.motorengine_plugin import MotorEnginePlugin
from preggy import expect
from mock import patch

from gaas import __version__
import gaas.server
from tests import TestCase


class GaasServerTestCase(TestCase):
    def test_healthcheck(self):
        response = self.fetch('/healthcheck')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like('WORKING')

    def test_version(self):
        response = self.fetch('/version')
        expect(response.code).to_equal(200)
        expect(response.body).to_be_like(__version__)

    def test_server_handlers(self):
        srv = gaas.server.GaasServer()
        handlers = srv.get_handlers()

        expect(handlers).not_to_be_null()
        expect(handlers).to_length(1)

    def test_server_plugins(self):
        srv = gaas.server.GaasServer()
        plugins = srv.get_plugins()

        expect(plugins).to_length(1)
        expect(plugins[0]).to_equal(MotorEnginePlugin)

    @patch('gaas.server.GaasServer')
    def test_server_main_function(self, server_mock):
        gaas.server.main()
        expect(server_mock.run.called).to_be_true()
