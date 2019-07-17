#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


setup(
    name='xivo-purge-db',
    version='1.2',
    description='XiVO database cleaner',
    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',
    url='http://wazo.community',
    license='GPLv3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'xivo-purge-db = xivo_purge_db.cli:main',
        ],
        'wazo_purge_db.purgers': [
            'call-log = xivo_purge_db.table_purger:CallLogPurger',
            'cel = xivo_purge_db.table_purger:CELPurger',
            'queue-log = xivo_purge_db.table_purger:QueueLogPurger',
            'stat-agent = xivo_purge_db.table_purger:StatAgentPeriodicPurger',
            'stat-call-on = xivo_purge_db.table_purger:StatCallOnQueuePurger',
            'stat-queue = xivo_purge_db.table_purger:StatQueuePeriodicPurger',
            'stat-switchboard = xivo_purge_db.table_purger:StatSwitchboardPurger',
        ]
    }
)
