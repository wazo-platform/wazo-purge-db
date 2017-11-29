# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from datetime import datetime, timedelta

from hamcrest import assert_that
from hamcrest import contains_inanyorder
from hamcrest import empty
from hamcrest import has_property

from xivo_dao.alchemy.call_log import CallLog as CallLogSchema
from xivo_dao.tests.test_dao import DAOTestCase
from xivo_purge_db.table_purger import CallLogPurger


class TestCallLogPurger(DAOTestCase):

    def setUp(self):
        super(TestCallLogPurger, self).setUp()

    def tearDown(self):
        super(TestCallLogPurger, self).tearDown()

    def add_call_log(self, **kwargs):
        kwargs.setdefault('id', self._generate_int())
        kwargs.setdefault('date', datetime.now())
        kwargs.setdefault('duration', timedelta(1))
        call_log = CallLogSchema(**kwargs)
        self.add_me(call_log)
        return call_log.id

    def test_that_CallLogPurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_call_log(date=current_time - timedelta(days=days_to_keep + 1))
        self.add_call_log(date=current_time - timedelta(days=days_to_keep + 2))
        self.add_call_log(date=current_time - timedelta(days=days_to_keep + 3))

        CallLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(CallLogSchema).all()

        assert_that(result, empty())

    def test_that_CallLogPurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_call_log(date=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_call_log(date=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_call_log(date=current_time - timedelta(days=days_to_keep - 3))

        CallLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(CallLogSchema).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry0),
                                                has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_CallLogPurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_call_log(date=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_call_log(date=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_call_log(date=current_time - timedelta(days=days_to_keep - 3))

        CallLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(CallLogSchema).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_CallLogPurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        CallLogPurger().purge(days_to_keep, self.session)

        result = self.session.query(CallLogSchema).all()

        assert_that(result, empty())
