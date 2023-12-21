#!/usr/bin/env python3
# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import find_packages, setup

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
        ],
        'wazo_purge_db.purgers': [
            'cel = wazo_purge_db.table_purger:CELPurger',
            'queue-log = wazo_purge_db.table_purger:QueueLogPurger',
            'stat-agent = wazo_purge_db.table_purger:StatAgentPeriodicPurger',
            'stat-call-on = wazo_purge_db.table_purger:StatCallOnQueuePurger',
            'stat-queue = wazo_purge_db.table_purger:StatQueuePeriodicPurger',
            'stat-switchboard = wazo_purge_db.table_purger:StatSwitchboardPurger',
        ],
    },
)
