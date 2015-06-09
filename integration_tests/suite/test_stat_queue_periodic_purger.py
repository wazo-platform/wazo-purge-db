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
from hamcrest import empty
from hamcrest import has_property
from hamcrest import contains_inanyorder

from xivo_dao.alchemy.stat_queue_periodic import StatQueuePeriodic as StatQueuePeriodicSchema
from xivo_dao.tests.test_dao import DAOTestCase
from xivo_purge_db.table_purger import StatQueuePeriodicPurger


class TestStatQueuePeriodicPurger(DAOTestCase):

    def setUp(self):
        super(TestStatQueuePeriodicPurger, self).setUp()

    def tearDown(self):
        super(TestStatQueuePeriodicPurger, self).tearDown()

    def add_stat_queue_periodic(self, **kwargs):
        kwargs.setdefault('id', self._generate_int())
        kwargs.setdefault('time', datetime.now())
        kwargs.setdefault('answered', 0)
        kwargs.setdefault('abandoned', 0)
        kwargs.setdefault('total', 0)
        kwargs.setdefault('full', 0)
        kwargs.setdefault('closed', 0)
        kwargs.setdefault('joinempty', 0)
        kwargs.setdefault('leaveempty', 0)
        kwargs.setdefault('divert_ca_ratio', 0)
        kwargs.setdefault('divert_waittime', 0)
        kwargs.setdefault('timeout', 0)
        stat_queue_periodic = StatQueuePeriodicSchema(**kwargs)
        self.add_me(stat_queue_periodic)
        return stat_queue_periodic.id

    def test_that_StatQueuePeriodicPurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 1))
        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 2))
        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 3))

        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(result, empty())

    def test_that_StatQueuePeriodicPurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 3))

        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry0),
                                                has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_StatQueuePeriodicPurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 3))

        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_StatQueuePeriodicPurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(result, empty())
