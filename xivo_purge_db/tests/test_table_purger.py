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

from xivo_dao.tests.test_dao import DAOTestCase
class TestTablePurger(DAOTestCase):

    def _insert_cels(self, cels):
        self.add_me_all(cels)

    def test_caller_id_by_unique_id_when_unique_id_is_present(self):
        self._insert_cels([
            _new_cel(eventtype='CHAN_START', cid_name='name1', cid_num='num1',
                     uniqueid='1'),
            _new_cel(eventtype='APP_START', cid_name='name2', cid_num='num2',
                     uniqueid='2'),
        ])

        self.assertEqual('"name2" <num2>', cel_dao.caller_id_by_unique_id('2'))

