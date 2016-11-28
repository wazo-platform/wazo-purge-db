#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


setup(
    name='xivo-purge-db',
    version='1.2',
    description='XiVO database cleaner',
    author='Avencall',
    author_email='dev@avencall.com',
    url='https://github.com/wazo-pbx/xivo-purge-db',
    license='GPLv3',
    packages=find_packages(),
    scripts=['bin/xivo-purge-db'],
)
