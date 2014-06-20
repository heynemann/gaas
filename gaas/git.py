#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os.path import abspath, join, exists, dirname

import pygit2


def create_git_repo(name, git_root):
    path = abspath(join(
        git_root,
        name
    ))

    if not exists(dirname(path)):
        os.makedirs(dirname(path))

    return pygit2.init_repository(path, False)


def clone(repo_url, repo_path, ref='refs/heads/master'):
    repo = pygit2.clone_repository(repo_url, repo_path)
    repo.checkout(ref)
    return repo
