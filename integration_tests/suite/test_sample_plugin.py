# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import subprocess
import textwrap

from hamcrest import assert_that
from hamcrest import is_
from unittest import TestCase

extra_config_path = '/etc/wazo-purge-db/conf.d'
extra_config_filename = 'extra-config-sample.yml'
extra_config_file = os.path.join(extra_config_path, extra_config_filename)

archive_output_file = '/tmp/wazo_purge_db.archive'
purge_output_file = '/tmp/wazo_purge_db.purge'

logger = logging.getLogger(__name__)


class TestSamplePlugin(TestCase):
    def setUp(self):
        extra_config = textwrap.dedent(
            """
            enabled_plugins:
                purgers:
                     sample: true
                archives:
                    - sample
            db_uri: 'postgresql://asterisk:proformatique@db/asterisk'
            days_to_keep: 123
            days_to_keep_per_plugin:
                sample: 30
            """
        )

        with open(extra_config_file, 'w') as config_file:
            config_file.write(extra_config)

    def tearDown(self):
        if os.path.exists(extra_config_file):
            self._run_cmd('rm {}'.format(extra_config_file))
        if os.path.exists(archive_output_file):
            self._run_cmd('rm {}'.format(archive_output_file))
        if os.path.exists(purge_output_file):
            self._run_cmd('rm {}'.format(purge_output_file))

    def _run_cmd(self, cmd):
        process = subprocess.Popen(
            cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        out, err = process.communicate()
        logger.info(out)

    def test_that_load_plugins_works_with_SamplePlugin(self):
        self._run_cmd('wazo-purge-db')

        file_exists = os.path.exists(archive_output_file)

        assert_that(file_exists, is_(True))

        with open(archive_output_file, 'r') as f:
            archive_content = f.read()
            assert_that(archive_content,
                        "Save tables before purge. 123 days to keep!")

        file_exists = os.path.exists(purge_output_file)

        assert_that(file_exists, is_(True))

        with open(purge_output_file, 'r') as f:
            purge_content = f.read()
            assert_that(purge_content, "Purged, 30 days keeped!")
