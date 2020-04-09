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

from io import StringIO
from unittest.mock import patch, MagicMock

import colorful as cf

from autohooks.terminal import Terminal


class TerminalTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        # getting the bash-color-codes from the colorful module
        self.red = cf.red.style[0]
        self.green = cf.green.style[0]
        self.yellow = cf.yellow.style[0]
        self.cyan = cf.cyan.style[0]
        self.reset = cf.black.style[
            1
        ]  # every colors second value is the reset value ...
        self.term = Terminal()
        self.term.get_width = MagicMock(return_value=80)

    @patch('sys.stdout', new_callable=StringIO)
    def test_error(self, mock_stdout):
        msg = 'foo bar'

        width = self.term.get_width()
        expected_len = width + len(self.red) + len(self.reset) + 1

        status = '[ {}error{} ]\n'.format(self.red, self.reset)
        sep = ' ' * (expected_len - len(msg) - len(status))

        expected_msg = msg + sep + status

        self.term.error(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), expected_len)
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_fail(self, mock_stdout):
        width = self.term.get_width()
        expected_len = width + len(self.red) + len(self.reset) + 1

        status = '[ {}fail{} ]\n'.format(self.red, self.reset)
        msg = 'foo bar baz'
        sep = ' ' * (expected_len - len(msg) - len(status))

        expected_msg = msg + sep + status

        self.term.fail('foo bar baz')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), expected_len)
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_info(self, mock_stdout):
        width = self.term.get_width()
        expected_len = width + len(self.cyan) + len(self.reset) + 1

        status = '[ {}info{} ]\n'.format(self.cyan, self.reset)
        msg = 'foo bar'
        sep = ' ' * (expected_len - len(msg) - len(status))

        expected_msg = msg + sep + status

        self.term.info('foo bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), expected_len)
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_ok(self, mock_stdout):
        width = self.term.get_width()
        expected_len = width + len(self.green) + len(self.reset) + 1

        status = '[ {}ok{} ]\n'.format(self.green, self.reset)
        msg = 'foo bar'
        sep = ' ' * (expected_len - len(msg) - len(status))
        expected_msg = msg + sep + status

        self.term.ok('foo bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), expected_len)
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_warning(self, mock_stdout):
        width = self.term.get_width()
        expected_len = width + len(self.yellow) + len(self.reset) + 1

        msg = 'foo bar'

        status = '[ {}warning{} ]\n'.format(self.yellow, self.reset)
        sep = ' ' * (expected_len - len(msg) - len(status))

        expected_msg = msg + sep + status

        self.term.warning(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), expected_len)
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print(self, mock_stdout):
        term = Terminal()

        expected_msg = 'foo bar\n'

        term.print('foo bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_indent(self, mock_stdout):
        term = Terminal()

        i = 6
        expected_msg = ' ' * i + 'foo\n'

        term.add_indent(i)
        term.print('foo')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        j = 4
        expected_msg = ' ' * (i + j) + 'bar\n'

        term.add_indent(j)
        term.print('bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_with_indent(self, mock_stdout):
        term = Terminal()

        expected_msg = '  foo\n'

        with term.indent(2):
            term.print('foo')

            ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        term.print('bar')

        expected_msg = 'bar\n'

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)


if __name__ == '__main__':
    unittest.main()
