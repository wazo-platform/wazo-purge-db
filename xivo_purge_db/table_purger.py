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

import abc
import datetime

from sqlalchemy import func
from xivo_dao.alchemy.call_log import CallLog
from xivo_dao.alchemy.cel import CEL
from xivo_dao.alchemy.queue_log import QueueLog
from xivo_dao.alchemy.stat_agent_periodic import StatAgentPeriodic
from xivo_dao.alchemy.stat_call_on_queue import StatCallOnQueue
from xivo_dao.alchemy.stat_queue_periodic import StatQueuePeriodic
from xivo_dao.alchemy.stat_switchboard_queue import StatSwitchboardQueue


class TablePurger(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def purge(self, days_to_keep, session):
        pass


class CallLogPurger(TablePurger):

    def purge(self, days_to_keep, session):
        query = (CallLog.__table__
                 .delete()
                 .where(CallLog.date
                        < (func.localtimestamp() - datetime.timedelta(days=days_to_keep)))
                 )
        session.execute(query)


class CELPurger(TablePurger):

    def purge(self, days_to_keep, session):
        query = (CEL.__table__
                 .delete()
                 .where(CEL.eventtime
                        < (func.localtimestamp() - datetime.timedelta(days=days_to_keep)))
                 )
        session.execute(query)


class QueueLogPurger(TablePurger):

    def purge(self, days_to_keep, session):
        query = (QueueLog.__table__
                 .delete()
                 .where(func.to_timestamp(QueueLog.time, 'YYYY-MM-DD HH24:MI:SS')
                        < (func.localtimestamp() - datetime.timedelta(days=days_to_keep)))
                 )
        session.execute(query)


class StatAgentPeriodicPurger(TablePurger):

    def purge(self, days_to_keep, session):
        query = (StatAgentPeriodic.__table__
                 .delete()
                 .where(StatAgentPeriodic.time
                        < (func.localtimestamp() - datetime.timedelta(days=days_to_keep)))
                 )
        session.execute(query)


class StatCallOnQueuePurger(TablePurger):

    def purge(self, days_to_keep, session):
        query = (StatCallOnQueue.__table__
                 .delete()
                 .where(StatCallOnQueue.time
                        < (func.localtimestamp() - datetime.timedelta(days=days_to_keep)))
                 )
        session.execute(query)


class StatQueuePeriodicPurger(TablePurger):

    def purge(self, days_to_keep, session):
        query = (StatQueuePeriodic.__table__
                 .delete()
                 .where(StatQueuePeriodic.time
                        < (func.localtimestamp() - datetime.timedelta(days=days_to_keep)))
                 )
        session.execute(query)


class StatSwitchboardPurger(TablePurger):

    def purge(self, days_to_keep, session):
        query = (StatSwitchboardQueue.__table__
                 .delete()
                 .where(StatSwitchboardQueue.time
                        < (func.localtimestamp() - datetime.timedelta(days=days_to_keep)))
                 )
        session.execute(query)
