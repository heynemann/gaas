#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class BaseStorage(object):
    __metaclass__ = ABCMeta

    def __init__(self, server, application, config, io_loop):
        self.server = server
        self.application = application
        self.config = config
        self.io_loop = io_loop

    def define_config(self, config):
        pass

    def initialize(self):
        pass

    @abstractmethod
    def connect(self, handler):
        pass

    @abstractmethod
    def disconnect(self, handler):
        pass

    def destruct(self):
        pass

    def migrate(self):
        pass
