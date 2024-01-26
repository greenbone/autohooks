# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# pylint: disable=invalid-name, protected-access

import os
import unittest
from io import StringIO
from unittest.mock import patch

from autohooks.terminal import Signs, Terminal


class TerminalTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["NO_COLOR"] = "1"
        os.environ["TERM"] = "unknown"
        self.maxDiff = 180
        self.term = Terminal()

    @patch("sys.stdout", new_callable=StringIO)
    def test_error(self, mock_stdout):
        msg = "foo bar"

        expected_msg = f" {Signs.ERROR} {msg}\n"

        self.term.error(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)

    @patch("sys.stdout", new_callable=StringIO)
    def test_fail(self, mock_stdout):
        msg = "foo bar baz"

        expected_msg = f" {Signs.FAIL} {msg}\n"

        self.term.fail(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)

    @patch("sys.stdout", new_callable=StringIO)
    def test_info(self, mock_stdout):
        msg = "foo bar"

        expected_msg = f" {Signs.INFO} {msg}\n"

        self.term.info(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)

    @patch("sys.stdout", new_callable=StringIO)
    def test_bold_info(self, mock_stdout):
        msg = "bold foo bar"

        expected_msg = f" {Signs.INFO} bold foo bar\n"

        self.term.bold_info(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)

    @patch("sys.stdout", new_callable=StringIO)
    def test_ok(self, mock_stdout):
        msg = "foo bar"

        expected_msg = f" {Signs.OK} {msg}\n"

        self.term.ok(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)

    @patch("sys.stdout", new_callable=StringIO)
    def test_warning(self, mock_stdout):
        msg = "foo bar"

        expected_msg = f" {Signs.WARNING} {msg}\n"

        self.term.warning(msg)

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print(self, mock_stdout):
        expected_msg = " foo bar\n"
        self.term.print("foo bar")

        ret = mock_stdout.getvalue()

        self.assertEqual(expected_msg, ret)

    @patch("sys.stdout", new_callable=StringIO)
    def test_with_indent(self, mock_stdout):
        expected_msg = "   foo\n"

        with self.term.indent(2):
            self.term.print("foo")

            ret = mock_stdout.getvalue()

        self.assertEqual(expected_msg, ret)

        # clear the buffer
        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        expected_msg = " bar\n"
        self.term.print("bar")

        ret = mock_stdout.getvalue()

        self.assertEqual(ret, expected_msg)


if __name__ == "__main__":
    unittest.main()
