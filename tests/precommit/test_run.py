# Copyright (C) 2022 Greenbone Networks GmbH
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

from autohooks.precommit.run import (
    CheckPluginError,
    CheckPluginWarning,
    check_plugin,
)
from tests import temp_python_module, tempdir


class CheckPluginTestCase(unittest.TestCase):
    def test_plugin_not_found(self):
        with tempdir(change_into=True):
            result = check_plugin("foo.bar")

            self.assertIsInstance(result, CheckPluginError)
            self.assertIn(
                '"foo.bar" is not a valid autohooks plugin.', result.message
            )

    def test_no_precommit_function(self):
        content = """print()"""
        with temp_python_module(
            content,
            name="foo",
        ):
            result = check_plugin("foo")

            self.assertIsInstance(result, CheckPluginError)
            self.assertEqual(
                result.message,
                'Plugin "foo" has no precommit function. The function is '
                "required to run the plugin as git pre commit hook.",
            )

    def test_no_precommit_function_arguments(self):
        content = """def precommit():
  print()"""
        with temp_python_module(
            content,
            name="foo",
        ):
            result = check_plugin("foo")

            self.assertIsInstance(result, CheckPluginWarning)
            self.assertEqual(
                'Plugin "foo" uses a deprecated signature for its precommit '
                "function. It is missing the **kwargs parameter.",
                result.message,
            )

    def test_success(self):
        content = """def precommit(**kwargs):
  print()"""
        with temp_python_module(
            content,
            name="foo",
        ):
            self.assertIsNone(check_plugin("foo"))
