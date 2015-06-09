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
