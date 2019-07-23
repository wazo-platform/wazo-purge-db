#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages


setup(
    name='wazo-purge-db',
    version='1.2',
    description='Wazo database cleaner',
    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',
    url='http://wazo.community',
    license='GPLv3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wazo-purge-db = wazo_purge_db.cli:main',
            'xivo-purge-db = wazo_purge_db.cli:main_compat',
        ],
        'wazo_purge_db.purgers': [
            'call-log = wazo_purge_db.table_purger:CallLogPurger',
            'cel = wazo_purge_db.table_purger:CELPurger',
            'queue-log = wazo_purge_db.table_purger:QueueLogPurger',
            'stat-agent = wazo_purge_db.table_purger:StatAgentPeriodicPurger',
            'stat-call-on = wazo_purge_db.table_purger:StatCallOnQueuePurger',
            'stat-queue = wazo_purge_db.table_purger:StatQueuePeriodicPurger',
            'stat-switchboard = wazo_purge_db.table_purger:StatSwitchboardPurger',
        ],
    },
)
