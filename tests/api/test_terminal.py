# Copyright (C) 2019 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from unittest.mock import Mock

from autohooks.api import _set_terminal, error, fail, info, ok, out, warning
from autohooks.terminal import Terminal


class TerminalOutputApiTestCase(unittest.TestCase):
    def setUp(self):
        self.term = Mock(spec=Terminal)
        _set_terminal(self.term)

    def test_error(self):
        error('foo bar')
        self.term.error.assert_called_with('foo bar')

    def test_fail(self):
        fail('foo bar')
        self.term.fail.assert_called_with('foo bar')

    def test_info(self):
        info('foo bar')
        self.term.info.assert_called_with('foo bar')

    def test_ok(self):
        ok('foo bar')
        self.term.ok.assert_called_with('foo bar')

    def test_out(self):
        out('foo bar')
        self.term.print.assert_called_with('foo bar')

    def test_warning(self):
        warning('foo bar')
        self.term.warning.assert_called_with('foo bar')


if __name__ == '__main__':
    unittest.main()
