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

# pylint: disable=invalid-name, protected-access

import unittest

import sys

from unittest.mock import Mock, MagicMock, patch

from autohooks.terminal import Terminal


class PropertyMagicMock(MagicMock):
    def __get__(self, obj, obj_type=None):
        return self()

    def __set__(self, obj, val):
        self(val)

    def _get_child_mock(self, **kwargs):
        return MagicMock(**kwargs)


class TerminalTestCase(unittest.TestCase):
    def assertCalled(self, mock):
        if sys.version_info[1] < 6:
            self.assertEqual(
                mock.call_count,
                1,
                '{} not called'.format(mock._mock_name or 'mock'),
            )
        else:
            mock.assert_called()

    def setUp(self):
        self.print_patcher = patch('builtins.print')
        self.terminal_patcher = patch('autohooks.terminal.Term', spec=True)

        terminal_mock_class = self.terminal_patcher.start()
        self.print_mock = self.print_patcher.start()

        self.width_mock = PropertyMagicMock(return_value=80, spec=1)

        self.terminal_mock = terminal_mock_class.return_value

        # "Because of the way mock attributes are stored you can’t directly
        #  attach a PropertyMock to a mock object. Instead you can attach it to
        #  the mock type object"
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock
        type(self.terminal_mock).width = self.width_mock

        self.terminal_mock.cyan = Mock()
        self.terminal_mock.green = Mock()
        self.terminal_mock.red = Mock()
        self.terminal_mock.yellow = Mock()

        self.terminal_mock.move_x = Mock()

    def tearDown(self):
        self.print_patcher.stop()
        self.terminal_patcher.stop()

    def test_error(self):
        term = Terminal()
        term.error('foo bar')

        # width has been calculated
        self.width_mock.assert_called_with()

        # 70 == 80 - 5 - len('error')
        self.terminal_mock.move_x.assert_called_with(70)

        # error has been printed in red
        self.terminal_mock.red.assert_called_with('error')

        # an actual output has been generated
        self.assertCalled(self.print_mock)

    def test_fail(self):
        term = Terminal()
        term.fail('foo bar')

        # width has been calculated
        self.width_mock.assert_called_with()

        # 71 == 80 - 5 - len('fail')
        self.terminal_mock.move_x.assert_called_with(71)

        # fail has been printed in red
        self.terminal_mock.red.assert_called_with('fail')

        # an actual output has been generated
        self.assertCalled(self.print_mock)

    def test_info(self):
        term = Terminal()
        term.info('foo bar')

        # width has been calculated
        self.width_mock.assert_called_with()

        # 71 == 80 - 5 - len('info')
        self.terminal_mock.move_x.assert_called_with(71)

        # info has been printed in cyan
        self.terminal_mock.cyan.assert_called_with('info')

        # an actual output has been generated
        self.assertCalled(self.print_mock)

    def test_ok(self):
        term = Terminal()
        term.ok('foo bar')

        # width has been calculated
        self.width_mock.assert_called_with()

        # 73 == 80 - 5 - len('ok')
        self.terminal_mock.move_x.assert_called_with(73)

        # ok has been printed in green
        self.terminal_mock.green.assert_called_with('ok')

        # an actual output has been generated
        self.assertCalled(self.print_mock)

    def test_warning(self):
        term = Terminal()
        term.warning('foo bar')

        # width has been calculated
        self.width_mock.assert_called_with()

        # 68 == 80 - 5 - len('warning')
        self.terminal_mock.move_x.assert_called_with(68)

        # warning has been printed in yellow
        self.terminal_mock.yellow.assert_called_with('warning')

        # an actual output has been generated
        self.assertCalled(self.print_mock)

    def test_print(self):
        term = Terminal()
        term.print('foo bar')

        # printed output at current indent location
        self.terminal_mock.location.assert_called_with(x=0)

        # an actual output has been generated
        self.print_mock.assert_called_with('foo bar')

    def test_add_indent(self):
        term = Terminal()
        term.add_indent(6)
        term.print('foo')

        # printed output at current indent location
        self.terminal_mock.location.assert_called_with(x=6)

        # an actual output has been generated
        self.print_mock.assert_called_with('foo')

        term.add_indent(4)
        term.print('bar')

        # printed output at current indent location
        self.terminal_mock.location.assert_called_with(x=10)

        # an actual output has been generated
        self.print_mock.assert_called_with('bar')

    def test_with_indent(self):
        term = Terminal()

        with term.indent(2):
            term.print('foo')

        self.terminal_mock.location.assert_called_with(x=2)
        self.print_mock.assert_called_with('foo')

        term.print('bar')

        # indentation has been removed
        self.terminal_mock.location.assert_called_with(x=0)
        self.print_mock.assert_called_with('bar')


if __name__ == '__main__':
    unittest.main()
