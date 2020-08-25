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

from autohooks.terminal import Terminal, Signs


class TerminalTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 180
        # getting the bash-color-codes from the colorful module
        self.red = cf.red
        self.green = cf.green
        self.yellow = cf.yellow
        self.cyan = cf.cyan
        self.reset = cf.reset
        self.bold = cf.bold
        # every colors second value is the reset value ...
        self.term = Terminal()
        self.term.get_width = MagicMock(return_value=80)

    @patch('sys.stdout', new_callable=StringIO)
    def test_error(self, mock_stdout):
        status = '{} '.format(self.red(Signs.ERROR))
        msg = 'foo bar'

        expected_msg = (
            self.reset('{}{}'.format(status, msg)).styled_string + '\n'
        )
        expected_len = len(expected_msg)

        self.term.error(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)
        self.assertEqual(len(ret), expected_len)

    @patch('sys.stdout', new_callable=StringIO)
    def test_fail(self, mock_stdout):
        status = '{} '.format(self.red(Signs.FAIL))
        msg = 'foo bar baz'

        expected_msg = (
            self.reset('{}{}'.format(status, msg)).styled_string + '\n'
        )
        expected_len = len(expected_msg)

        self.term.fail(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)
        self.assertEqual(len(ret), expected_len)

    @patch('sys.stdout', new_callable=StringIO)
    def test_info(self, mock_stdout):
        status = '{} '.format(self.cyan(Signs.INFO))
        msg = 'foo bar'

        expected_msg = (
            self.reset('{}{}'.format(status, msg)).styled_string + '\n'
        )
        expected_len = len(expected_msg)

        self.term.info(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)
        self.assertEqual(len(ret), expected_len)

    @patch('sys.stdout', new_callable=StringIO)
    def test_bold_info(self, mock_stdout):
        status = '{} '.format(self.cyan(Signs.INFO))
        msg = 'bold foo bar'

        expected_msg = (
            self.bold('{}{}'.format(status, msg)).styled_string + '\n'
        )
        expected_len = len(expected_msg)

        self.term.bold_info(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)
        self.assertEqual(len(ret), expected_len)

    @patch('sys.stdout', new_callable=StringIO)
    def test_ok(self, mock_stdout):
        status = '{} '.format(self.green(Signs.OK))
        msg = 'foo bar'

        expected_msg = (
            self.reset('{}{}'.format(status, msg)).styled_string + '\n'
        )
        expected_len = len(expected_msg)

        self.term.ok(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)
        self.assertEqual(len(ret), expected_len)

    @patch('sys.stdout', new_callable=StringIO)
    def test_warning(self, mock_stdout):
        msg = 'foo bar'

        status = '{} '.format(self.yellow(Signs.WARNING))

        expected_msg = (
            self.reset('{}{}'.format(status, msg)).styled_string + '\n'
        )
        expected_len = len(expected_msg)

        self.term.warning(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)
        self.assertEqual(len(ret), expected_len)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print(self, mock_stdout):
        expected_msg = self.reset('  foo bar').styled_string + '\n'

        self.term.print('foo bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_indent(self, mock_stdout):
        i = 6
        expected_msg = self.reset(' ' * i + 'foo').styled_string + '\n'

        self.term.add_indent(i - 2)
        self.term.print('foo')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        j = 4
        expected_msg = self.reset(' ' * (i + j) + 'bar').styled_string + '\n'

        self.term.add_indent(j)
        self.term.print('bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_reset_indent(self, mock_stdout):
        i = 6
        expected_msg = self.reset(' ' * i + 'foo').styled_string + '\n'

        self.term.add_indent(i - 2)
        self.term.print('foo')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        expected_msg = self.reset('  bar').styled_string + '\n'

        self.term.reset_indent()
        self.term.print('bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_with_indent(self, mock_stdout):
        expected_msg = self.reset('    foo').styled_string + '\n'

        with self.term.indent(2):
            self.term.print('foo')

            ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        expected_msg = self.reset('  bar').styled_string + '\n'
        self.term.print('bar')

        ret = mock_stdout.getvalue()

        self.assertEqual(len(ret), len(expected_msg))
        self.assertEqual(ret, expected_msg)

    @patch('sys.stdout', new_callable=StringIO)
    def test_long_msg(self, mock_stdout):
        long_msg = (
            'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, '
            'sed diam nonumy eirmod tempor invidunt ut labore et dolore magna'
            ' aliquyam erat, sed diam voluptua.'
        )
        expected_msg = (
            self.reset(
                '  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, '
                'sed diam nonumy eirmo\n  d tempor invidunt ut labore et'
                ' dolore magna aliquyam erat, sed diam voluptua.'
            ).styled_string
            + '\n'
        )
        expected_len = len(expected_msg)

        self.term.print(long_msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)
        self.assertEqual(len(ret), expected_len)


if __name__ == '__main__':
    unittest.main()
