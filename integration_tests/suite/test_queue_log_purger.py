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

from xivo_dao.alchemy.queue_log import QueueLog as QueueLogSchema
from xivo_dao.tests.test_dao import DAOTestCase
from xivo_purge_db.table_purger import QueueLogPurger


class TestQueueLogPurger(DAOTestCase):

    def setUp(self):
        super(TestQueueLogPurger, self).setUp()

    def tearDown(self):
        super(TestQueueLogPurger, self).tearDown()

    def add_queue_log(self, **kwargs):
        kwargs.setdefault('id', self._generate_int())
        kwargs.setdefault('time', datetime.now())
        kwargs.setdefault('callid', self._generate_int())
        kwargs.setdefault('queuename', self._random_name())
        kwargs.setdefault('agent', self._random_name())
        kwargs.setdefault('event', self._random_name())
        queue_log = QueueLogSchema(**kwargs)
        self.add_me(queue_log)
        return queue_log.id

    def test_that_QueueLogPurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_queue_log(time=current_time - timedelta(days=days_to_keep + 1))
        self.add_queue_log(time=current_time - timedelta(days=days_to_keep + 2))
        self.add_queue_log(time=current_time - timedelta(days=days_to_keep + 3))

        QueueLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(QueueLogSchema).all()

        assert_that(result, empty())

    def test_that_QueueLogPurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_queue_log(time=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_queue_log(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_queue_log(time=current_time - timedelta(days=days_to_keep - 3))

        QueueLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(QueueLogSchema).all()

        assert_that(result, only_contains(
            all_of(has_property('id', id_entry0)),
            all_of(has_property('id', id_entry1)),
            all_of(has_property('id', id_entry2)),
            ))

    def test_that_QueueLogPurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_queue_log(time=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_queue_log(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_queue_log(time=current_time - timedelta(days=days_to_keep - 3))

        QueueLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(QueueLogSchema).all()

        assert_that(result, only_contains(
            all_of(has_property('id', id_entry1)),
            all_of(has_property('id', id_entry2)),
            ))

    def test_that_QueueLogPurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        QueueLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(QueueLogSchema).all()

        assert_that(result, empty())
