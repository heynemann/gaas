#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from gaas import __version__

tests_require = [
    'nose',
    'mock',
    'coverage',
    'rednose',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
    'factory_boy',
    'alembic',
    'nose_focus',
    'mysql-python',
]

setup(
    name='gaas',
    version=__version__,
    description="gaas is an acronym for Git as a service.",
    long_description="""gaas is an acronym for Git as a service.""",
    keywords='git repository management web saas',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='https://github.com/heynemann/gaas',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'pymongo==2.7',
        'pycurl',
        'cow-framework',
        'motorengine',
        'pygit2',
        'gittornado',
        'python-slugify'
    ],

    extras_require={
        'tests': tests_require,
    },

    entry_points={
        'console_scripts': [
            'gaas=gaas.server:main',
        ],
    }
)
