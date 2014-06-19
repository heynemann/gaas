#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.concurrent import return_future
import factory

from gaas.models.repository import Repository


class MotorEngineFactory(factory.base.Factory):
    """Factory for motorengine objects."""
    ABSTRACT_FACTORY = True

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        return target_class(*args, **kwargs)

    @classmethod
    @return_future
    def _create(cls, target_class, *args, **kwargs):
        callback = kwargs.get('callback', None)
        del kwargs['callback']
        instance = target_class(*args, **kwargs)
        instance.save(callback=callback)


class RepositoryFactory(MotorEngineFactory):
    FACTORY_FOR = Repository

    name = factory.Sequence(lambda n: 'repository_{0}'.format(n))
