#!/usr/bin/python
# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

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


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(2000), nullable=False)
    slug = sa.Column('slug', sa.String(2000), nullable=False)
    created_at = sa.Column(
        'created_at', sa.DateTime,
        default=datetime.utcnow, nullable=False
    )
