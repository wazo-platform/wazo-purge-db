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

from datetime import datetime, timedelta

from hamcrest import assert_that
from hamcrest import contains_inanyorder
from hamcrest import empty
from hamcrest import has_property

from xivo_dao.alchemy.cel import CEL as CELSchema
from xivo_dao.tests.test_dao import DAOTestCase
from xivo_purge_db.table_purger import CELPurger


class TestCELPurger(DAOTestCase):

    def setUp(self):
        super(TestCELPurger, self).setUp()

    def tearDown(self):
        super(TestCELPurger, self).tearDown()

    def test_that_CELPurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 1))
        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 2))
        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 3))

        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(result, empty())

    def test_that_CELPurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 3))

        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry0),
                                                has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_CELPurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_cel(eventtime=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_cel(eventtime=current_time - timedelta(days=days_to_keep - 3))

        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_CELPurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        CELPurger().purge(days_to_keep, self.session)

        result = self.session.query(CELSchema).all()

        assert_that(result, empty())
