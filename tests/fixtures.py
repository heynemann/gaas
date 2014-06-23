#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.concurrent import return_future
import factory
import factory.alchemy

from gaas.storage.sqlalchemy import models as SaModels


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


class SqlAlchemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        instance = super(SqlAlchemyFactory, cls)._create(
            target_class, *args, **kwargs
        )
        if hasattr(cls, 'FACTORY_SESSION') and cls.FACTORY_SESSION is not None:
            cls.FACTORY_SESSION.flush()
        return instance


class SaRepositoryFactory(SqlAlchemyFactory):
    FACTORY_FOR = SaModels.Repository

    name = factory.Sequence(lambda n: 'repository {0}'.format(n))
    slug = factory.Sequence(lambda n: 'repository-{0}'.format(n))


class SaUserFactory(SqlAlchemyFactory):
    FACTORY_FOR = SaModels.User

    name = factory.Sequence(lambda n: 'user {0}'.format(n))
    slug = factory.Sequence(lambda n: 'user-{0}'.format(n))


class SaKeyFactory(SqlAlchemyFactory):
    FACTORY_FOR = SaModels.Key

    public_key = factory.Sequence(lambda n: 'key-{0}'.format(n))
    user = factory.SubFactory(SaUserFactory)
