# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

import logging

logger = logging.getLogger(__name__)


class DataPurger(object):

    def __init__(self, table_purgers):
        self.table_purgers = table_purgers

    def delete_old_entries(self, days_to_keep, session):
        logger.info('Deleting entries older than {0} days'.format(days_to_keep))
        for table in self.table_purgers:
            table.purge(days_to_keep, session)
            logger.debug('{purger} executed'.format(purger=table.__class__.__name__))
