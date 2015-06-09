#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


setup(
    name='xivo-purge-db-sample-plugin',
    version='1.1',
    description='XiVO sample plugin for archive before database clean',
    author='Avencall',
    author_email='dev@avencall.com',
    url='https://github.com/xivo-pbx/xivo-purge-db',
    license='GPLv3',
    packages=find_packages(),
    entry_points={
        'xivo_purge_db.archives': [
            'sample = xivo_purge_db_sample.sample:SamplePlugin',
        ],
    }
)
