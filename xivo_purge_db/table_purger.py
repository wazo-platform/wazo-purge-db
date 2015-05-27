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


class TablePurger(object):

    __metaclass__ = abc.ABCMeta

    TABLE_NAME = ''
    DATE_FIELD = ''
    DATE_FORMAT = ''
    QUERY = "DELETE FROM {0} WHERE time < ({1} - INTERVAL '{2} days')"

    @abc.abstractmethod
    def purge(self):
        pass


class CelPurger(TablePurger):

    TABLE_NAME = 'cel'
    DATE_FIELD = 'eventtime'
    DATE_FORMAT = ''

    def purge(self):
        pass


class CallLogPurger(TablePurger):

    TABLE_NAME = 'call_log'
    DATE_FIELD = 'current_date'
    DATE_FORMAT = ''

    def purge(self):
        pass
