# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from mock import Mock
from unittest import TestCase

from xivo_purge_db.data_purger import DataPurger


class TestDataPurger(TestCase):

    def setUp(self):
        self.purger1, self.purger2, self.purger3 = Mock(), Mock(), Mock()
        table_purgers = [self.purger1, self.purger2, self.purger3]
        self.data_purger = DataPurger(table_purgers)

    def test_that_DataPurger_call_every_purger(self):
        days_to_keep = 365
        session = Mock()

        self.data_purger.delete_old_entries(days_to_keep, session)

        self.purger1.purge.assert_called_once_with(days_to_keep, session)
        self.purger2.purge.assert_called_once_with(days_to_keep, session)
        self.purger3.purge.assert_called_once_with(days_to_keep, session)
