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
import os
from io import StringIO
from unittest.mock import patch

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

    @patch('sys.stdout', new_callable=StringIO)
    def test_error(self, mock_stdout):
        term = Terminal()

        width, _ = os.get_terminal_size()
        est_len = width + len(self.red) + len(self.reset) + 1

        term.error('foo bar')

        ret = mock_stdout.getvalue()
        status = '[ {}error{} ]\n'.format(self.red, self.reset)
        msg = 'foo bar'
        sep = ' ' * (est_len - (len(msg) + len(status)))

        reg = msg + sep + status

        self.assertIsNotNone(term._width)
        self.assertEqual(term._width, width)
        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, reg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_fail(self, mock_stdout):
        term = Terminal()

        width, _ = os.get_terminal_size()
        est_len = width + len(self.red) + len(self.reset) + 1

        term.fail('foo bar baz')

        ret = mock_stdout.getvalue()
        status = '[ {}fail{} ]\n'.format(self.red, self.reset)
        msg = 'foo bar baz'
        sep = ' ' * (est_len - (len(msg) + len(status)))

        reg = msg + sep + status

        self.assertIsNotNone(term._width)
        self.assertEqual(term._width, width)
        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, reg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_info(self, mock_stdout):
        term = Terminal()

        width, _ = os.get_terminal_size()
        est_len = width + len(self.cyan) + len(self.reset) + 1

        term.info('foo bar')

        ret = mock_stdout.getvalue()
        status = '[ {}info{} ]\n'.format(self.cyan, self.reset)
        msg = 'foo bar'
        sep = ' ' * (est_len - (len(msg) + len(status)))

        reg = msg + sep + status

        self.assertIsNotNone(term._width)
        self.assertEqual(term._width, width)
        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, reg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_ok(self, mock_stdout):
        term = Terminal()

        width, _ = os.get_terminal_size()
        est_len = width + len(self.green) + len(self.reset) + 1

        term.ok('foo bar')

        # get the printed output
        ret = mock_stdout.getvalue()

        # build the estimated output
        status = '[ {}ok{} ]\n'.format(self.green, self.reset)
        msg = 'foo bar'
        sep = ' ' * (est_len - (len(msg) + len(status)))
        reg = msg + sep + status

        # assert length and output and terminal width
        self.assertIsNotNone(term._width)
        self.assertEqual(term._width, width)
        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, reg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_warning(self, mock_stdout):
        term = Terminal()

        width, _ = os.get_terminal_size()
        est_len = width + len(self.yellow) + len(self.reset) + 1

        term.warning('foo bar')

        ret = mock_stdout.getvalue()
        status = '[ {}warning{} ]\n'.format(self.yellow, self.reset)
        msg = 'foo bar'
        sep = ' ' * (est_len - (len(msg) + len(status)))

        reg = msg + sep + status

        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, reg)
        self.assertIsNotNone(term._width)
        self.assertEqual(term._width, width)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print(self, mock_stdout):
        term = Terminal()

        msg = 'foo bar\n'
        est_len = len(msg)

        term.print('foo bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_indent(self, mock_stdout):
        term = Terminal()
        i = 6
        msg = ' ' * i + 'foo\n'
        est_len = len(msg)

        term.add_indent(i)
        term.print('foo')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        j = 4
        msg = ' ' * (i + j) + 'bar\n'
        est_len = len(msg)
        term.add_indent(j)
        term.print('bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_with_indent(self, mock_stdout):
        term = Terminal()

        with term.indent(2):
            msg = '  foo\n'
            est_len = len(msg)
            term.print('foo')

            ret = mock_stdout.getvalue()

            # self.assertEqual(len(ret), est_len)
            self.assertEqual(ret, msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        term.print('bar')

        msg = 'bar\n'
        est_len = len(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), est_len)
        self.assertEqual(ret, msg)


if __name__ == '__main__':
    unittest.main()
