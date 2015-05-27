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

import argparse
import logging
import xivo_dao

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy
from xivo.daemonize import pidfile_context
from xivo.xivo_logging import setup_logging
from xivo_purge_db.data_purger import DataPurger
from xivo_purge_db.table_purger import CelPurger, CallLogPurger

PIDFILENAME = '/var/run/xivo-purge-db.pid'
_DEFAULT_CONFIG = {
    'logfile': '/var/log/xivo-purge-db.log',
    'pidfile': '/var/run/xivo-purge-db.pid',
    'config_file': '/etc/xivo-purge-db/config.yml',
    'extra_config_files': '/etc/xivo-purge-db/conf.d',
    'debug': False,
}

logger = logging.getLogger(__name__)


def main():
    cli_config = _parse_args()
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    config = ChainMap(cli_config, file_config, _DEFAULT_CONFIG)

    setup_logging(config['logfile'], True, config['debug'])

    xivo_dao.init_db_from_config(config)

    with pidfile_context(PIDFILENAME, foreground=True):
        _purge_tables(config['days_to_keep'])


def _purge_tables(days_to_keep):
    table_purgers = []
    table_purgers.append(CelPurger())
    table_purgers.append(CallLogPurger())

    data_purger = DataPurger(days_to_keep, table_purgers)
    data_purger.delete_old_entries()


def _parse_args():
    config = {}
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--days_to_keep',
                        help='Number of days data will be kept in tables')

    parsed_args = parser.parse_args()
    if parsed_args.days_to_keep:
        config['days_to_keep'] = parsed_args.days_to_keep

    return config
