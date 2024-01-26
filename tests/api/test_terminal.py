# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from unittest.mock import Mock

from autohooks.api import error, fail, info, ok, out, warning
from autohooks.terminal import Terminal, _set_terminal


class TerminalOutputApiTestCase(unittest.TestCase):
    def setUp(self):
        self.term = Mock(spec=Terminal)
        _set_terminal(self.term)

    def test_error(self):
        error("foo bar")
        self.term.error.assert_called_with("foo bar")

    def test_fail(self):
        fail("foo bar")
        self.term.fail.assert_called_with("foo bar")

    def test_info(self):
        info("foo bar")
        self.term.info.assert_called_with("foo bar")

    def test_ok(self):
        ok("foo bar")
        self.term.ok.assert_called_with("foo bar")

    def test_out(self):
        out("foo bar")
        self.term.out.assert_called_with("foo bar")

    def test_warning(self):
        warning("foo bar")
        self.term.warning.assert_called_with("foo bar")


if __name__ == "__main__":
    unittest.main()
