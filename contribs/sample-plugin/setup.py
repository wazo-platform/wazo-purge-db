#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='wazo-purge-db-sample-plugin',
    version='1.1',
    description='XiVO sample plugin for archive before database clean',
    author='Avencall',
    author_email='dev@avencall.com',
    url='https://github.com/wazo-platform/wazo-purge-db',
    license='GPLv3',
    packages=find_packages(),
    entry_points={
        'wazo_purge_db.archives': [
            'sample = wazo_purge_db_sample.sample:archive_plugin'
        ],
        'wazo_purge_db.purgers': ['sample = wazo_purge_db_sample.sample:PurgePlugin'],
    },
)
