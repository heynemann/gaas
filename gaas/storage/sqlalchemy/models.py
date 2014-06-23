#!/usr/bin/python
# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Repository(Base):
    __tablename__ = "repositories"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(2000), nullable=False)
    slug = sa.Column('slug', sa.String(2000), nullable=False)
    uuid = sa.Column('uuid', sa.String(36), default=uuid4, nullable=False)
    created_at = sa.Column(
        'created_at', sa.DateTime,
        default=datetime.utcnow, nullable=False
    )


class Key(Base):
    __tablename__ = "keys"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    public_key = sa.Column('public_key', sa.String(512), nullable=False)
    created_at = sa.Column(
        'created_at', sa.DateTime,
        default=datetime.utcnow, nullable=False
    )


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(2000), nullable=False)
    slug = sa.Column('slug', sa.String(2000), nullable=False)
    created_at = sa.Column(
        'created_at', sa.DateTime,
        default=datetime.utcnow, nullable=False
    )

    keys = relationship(Key, backref="user")
