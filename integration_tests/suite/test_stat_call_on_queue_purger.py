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

from hamcrest import all_of, assert_that, empty, has_property, only_contains

from xivo_dao.alchemy.stat_call_on_queue import StatCallOnQueue as StatCallOnQueueSchema
from xivo_dao.tests.test_dao import DAOTestCase
from xivo_purge_db.table_purger import StatCallOnQueuePurger


class TestStatCallOnQueuePurger(DAOTestCase):

    def setUp(self):
        super(TestStatCallOnQueuePurger, self).setUp()

    def tearDown(self):
        super(TestStatCallOnQueuePurger, self).tearDown()

    def add_stat_call_on_queue(self, **kwargs):
        kwargs.setdefault('id', self._generate_int())
        kwargs.setdefault('time', datetime.now())
        kwargs.setdefault('callid', self._generate_int())
        kwargs.setdefault('ringtime', 0)
        kwargs.setdefault('talktime', 0)
        kwargs.setdefault('waittime', 0)
        kwargs.setdefault('status', 'answered')
        stat_call_on_queue = StatCallOnQueueSchema(**kwargs)
        self.add_me(stat_call_on_queue)
        return stat_call_on_queue.id

    def test_that_StatCallOnQueuePurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 1))
        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 2))
        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 3))

        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(result, empty())

    def test_that_StatCallOnQueuePurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 3))

        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(result, only_contains(
            all_of(has_property('id', id_entry0)),
            all_of(has_property('id', id_entry1)),
            all_of(has_property('id', id_entry2)),
            ))

    def test_that_StatCallOnQueuePurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 3))

        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(result, only_contains(
            all_of(has_property('id', id_entry1)),
            all_of(has_property('id', id_entry2)),
            ))

    def test_that_StatCallOnQueuePurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(result, empty())
