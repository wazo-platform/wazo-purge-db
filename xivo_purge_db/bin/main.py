# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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

from stevedore import enabled
from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy
from xivo.daemonize import pidfile_context
from xivo.xivo_logging import setup_logging
from xivo_dao.helpers.db_utils import session_scope
from xivo_purge_db.data_purger import DataPurger
from xivo_purge_db.table_purger import CallLogPurger
from xivo_purge_db.table_purger import CELPurger
from xivo_purge_db.table_purger import QueueLogPurger
from xivo_purge_db.table_purger import StatAgentPeriodicPurger
from xivo_purge_db.table_purger import StatCallOnQueuePurger
from xivo_purge_db.table_purger import StatQueuePeriodicPurger
from xivo_purge_db.table_purger import StatSwitchboardPurger


_DEFAULT_CONFIG = {
    'config_file': '/etc/xivo-purge-db/config.yml',
    'extra_config_files': '/etc/xivo-purge-db/conf.d/'
}

logger = logging.getLogger(__name__)


def main():
    cli_config = _parse_args()
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    config = ChainMap(cli_config, file_config, _DEFAULT_CONFIG)

    setup_logging(config['log_file'], foreground=True, debug=config['debug'])

    xivo_dao.init_db_from_config(config)

    with pidfile_context(config['pid_file'], foreground=True):
        if 'archives' in config.get('enabled_plugins', {}):
            _load_plugins(config)
        _purge_tables(config['days_to_keep'])


def _load_plugins(config):
    enabled_archives = config['enabled_plugins']['archives']
    check_func = lambda extension: extension.name in enabled_archives
    enabled.EnabledExtensionManager(namespace='xivo_purge_db.archives',
                                    check_func=check_func,
                                    invoke_args=(config,),
                                    invoke_on_load=True)


def _purge_tables(days_to_keep):
    table_purgers = []
    table_purgers.append(CallLogPurger())
    table_purgers.append(CELPurger())
    table_purgers.append(QueueLogPurger())
    table_purgers.append(StatAgentPeriodicPurger())
    table_purgers.append(StatCallOnQueuePurger())
    table_purgers.append(StatQueuePeriodicPurger())
    table_purgers.append(StatSwitchboardPurger())

    data_purger = DataPurger(table_purgers)

    with session_scope() as session:
        data_purger.delete_old_entries(days_to_keep, session)


def _parse_args():
    config = {}
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--days_to_keep',
                        type=int,
                        help='Number of days data will be kept in tables')

    parsed_args = parser.parse_args()
    if parsed_args.days_to_keep is not None:
        config['days_to_keep'] = parsed_args.days_to_keep

    return config
