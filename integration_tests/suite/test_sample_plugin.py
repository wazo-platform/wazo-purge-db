# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import os
import subprocess
import textwrap

from hamcrest import assert_that
from hamcrest import is_
from unittest import TestCase

extra_config_path = '/etc/xivo-purge-db/conf.d'
extra_config_filename = 'extra-config-sample'
extra_config_file = os.path.join(extra_config_path, extra_config_filename)

sample_output_file = '/tmp/xivo_purge_db.sample'

logger = logging.getLogger(__name__)


class TestSamplePlugin(TestCase):

    def setUp(self):
        extra_config = textwrap.dedent("""
            enabled_plugins:
                archives:
                    - sample
            db_uri: 'postgresql://asterisk:proformatique@db/asterisk'
            """)

        with open(extra_config_file, 'w') as config_file:
            config_file.write(extra_config)

    def tearDown(self):
        if os.path.exists(extra_config_file):
            self._run_cmd('rm {}'.format(extra_config_file))
        if os.path.exists(sample_output_file):
            self._run_cmd('rm {}'.format(sample_output_file))

    def _run_cmd(self, cmd):
        process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = process.communicate()
        logger.info(out)

    def test_that_load_plugins_works_with_SamplePlugin(self):
        self._run_cmd('xivo-purge-db')

        file_exists = os.path.exists(sample_output_file)

        assert_that(file_exists, is_(True))
