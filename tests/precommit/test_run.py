# SPDX-FileCopyrightText: 2022-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


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
