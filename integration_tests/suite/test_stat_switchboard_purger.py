# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from datetime import datetime, timedelta

from hamcrest import assert_that
from hamcrest import contains_inanyorder
from hamcrest import empty
from hamcrest import has_property

from xivo_dao.alchemy.queuefeatures import QueueFeatures
from xivo_dao.alchemy.stat_switchboard_queue import StatSwitchboardQueue
from xivo_dao.tests.test_dao import DAOTestCase
from xivo_purge_db.table_purger import StatSwitchboardPurger


class TestStatSwitchboardPurger(DAOTestCase):

    def setUp(self):
        super(TestStatSwitchboardPurger, self).setUp()
        self.stat_switchboard_queue = QueueFeatures(name='stat_switchboard_queue',
                                                    displayname='stat_switchboard_queue',
                                                    number='3333',
                                                    context='default',
                                                    tenant_uuid=self.default_tenant.uuid)
        self.add_me(self.stat_switchboard_queue)

    def add_stat_switchboard(self, **kwargs):
        kwargs.setdefault('id', self._generate_int())
        kwargs.setdefault('time', datetime.now())
        kwargs.setdefault('end_type', 'abandoned')
        kwargs.setdefault('wait_time', 1)
        kwargs.setdefault('queue_id', self.stat_switchboard_queue.id)
        stat_switchboard = StatSwitchboardQueue(**kwargs)
        self.add_me(stat_switchboard)
        return stat_switchboard.id

    def test_that_purger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep + 1))
        self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep + 2))
        self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep + 3))

        StatSwitchboardPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatSwitchboardQueue).all()

        assert_that(result, empty())

    def test_that_purger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep - 3))

        StatSwitchboardPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatSwitchboardQueue).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry0),
                                                has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_purger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_switchboard(time=current_time - timedelta(days=days_to_keep - 3))

        StatSwitchboardPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatSwitchboardQueue).all()

        assert_that(result, contains_inanyorder(has_property('id', id_entry1),
                                                has_property('id', id_entry2)))

    def test_that_purger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        StatSwitchboardPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatSwitchboardQueue).all()

        assert_that(result, empty())
