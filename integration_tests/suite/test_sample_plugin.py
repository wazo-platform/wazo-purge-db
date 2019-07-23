# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

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

sample_output_file = '/tmp/wazo_purge_db.sample'

logger = logging.getLogger(__name__)


class TestSamplePlugin(TestCase):
    def setUp(self):
        extra_config = textwrap.dedent(
            """
            enabled_plugins:
                archives:
                    - sample
            db_uri: 'postgresql://asterisk:proformatique@db/asterisk'
            """
        )

        with open(extra_config_file, 'w') as config_file:
            config_file.write(extra_config)

    def tearDown(self):
        if os.path.exists(extra_config_file):
            self._run_cmd('rm {}'.format(extra_config_file))
        if os.path.exists(sample_output_file):
            self._run_cmd('rm {}'.format(sample_output_file))

    def _run_cmd(self, cmd):
        process = subprocess.Popen(
            cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        out, err = process.communicate()
        logger.info(out)

    def test_that_load_plugins_works_with_SamplePlugin(self):
        self._run_cmd('wazo-purge-db')

        file_exists = os.path.exists(sample_output_file)

        assert_that(file_exists, is_(True))
