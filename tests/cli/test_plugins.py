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
from argparse import Namespace
from unittest.mock import MagicMock, call

from autohooks.cli.plugins import add_plugins, list_plugins, remove_plugins
from tests import temp_file, tempdir, unload_module


class AddPluginsCliTestCase(unittest.TestCase):
    def test_add_plugin(self):
        term = MagicMock()
        args = Namespace(name=["foo", "bar"])

        expected = """[tool.autohooks]
mode = "pythonpath"
pre-commit = ["bar", "foo"]
"""

        with tempdir(change_into=True) as tmp_dir:
            add_plugins(term, args)

            term.warning.assert_not_called()
            term.info.assert_has_calls([call("Added plugins:")])
            term.ok.assert_has_calls([call('"bar"'), call('"foo"')])

            pyproject_toml = tmp_dir / "pyproject.toml"
            content = pyproject_toml.read_text(encoding="utf8")

            self.assertEqual(content, expected)

    def test_add_plugin_with_existing(self):
        term = MagicMock()
        args = Namespace(name=["foo"])
        existing = """[tool.autohooks]
mode = "poetry"
pre-commit = ["bar"]
"""

        expected = """[tool.autohooks]
mode = "poetry"
pre-commit = ["bar", "foo"]
"""

        with temp_file(
            existing, name="pyproject.toml", change_into=True
        ) as pyproject_toml:
            add_plugins(term, args)

            term.warning.assert_not_called()
            term.info.assert_has_calls(
                [call("Added plugins:"), call("Currently used plugins:")]
            )
            term.ok.assert_has_calls([call('"foo"')])

            content = pyproject_toml.read_text(encoding="utf8")

            self.assertEqual(content, expected)

    def test_add_duplicate_plugin(self):
        term = MagicMock()
        args = Namespace(name=["foo", "bar"])
        existing = """[tool.autohooks]
mode = "poetry"
pre-commit = ["bar"]
"""

        expected = """[tool.autohooks]
mode = "poetry"
pre-commit = ["bar", "foo"]
"""

        with temp_file(
            existing, name="pyproject.toml", change_into=True
        ) as pyproject_toml:
            add_plugins(term, args)

            term.warning.assert_has_calls([call('"bar"')])
            term.info.assert_has_calls(
                [
                    call("Skipped already used plugins:"),
                    call("Added plugins:"),
                    call("Currently used plugins:"),
                ]
            )
            term.ok.assert_has_calls([call('"foo"')])

            content = pyproject_toml.read_text(encoding="utf8")

            self.assertEqual(content, expected)


class ListPluginsCliTestCase(unittest.TestCase):
    def setUp(self) -> None:
        unload_module("bar")
        return super().setUp()

    def test_invalid_plugins(self):
        term = MagicMock()
        args = Namespace()

        existing = """[tool.autohooks]
mode = "poetry"
pre-commit = ["bar"]
"""
        with temp_file(existing, name="pyproject.toml", change_into=True):
            list_plugins(term, args)

            term.warning.assert_not_called()
            term.info.assert_has_calls(
                [
                    call("Currently used plugins:"),
                ]
            )
            term.ok.assert_not_called()
            term.error.assert_called_once_with(
                '"bar": "bar" is not a valid autohooks plugin. No module '
                "named 'bar'"
            )

    def test_existing_plugins(self):
        term = MagicMock()
        args = Namespace()

        pyproject_toml_content = """[tool.autohooks]
mode = "poetry"
pre-commit = ["bar"]
"""

        plugin_content = """
def precommit(config=None, **kwargs):
    pass
"""
        with tempdir(change_into=True, add_to_sys_path=True) as tmp_dir:
            pyproject_toml = tmp_dir / "pyproject.toml"
            pyproject_toml.write_text(pyproject_toml_content, encoding="utf8")

            bar_plugin = tmp_dir / "bar.py"
            bar_plugin.write_text(plugin_content, encoding="utf8")

            list_plugins(term, args)

            term.warning.assert_not_called()
            term.info.assert_has_calls(
                [
                    call("Currently used plugins:"),
                ]
            )
            term.error.assert_not_called()
            term.ok.assert_called_once_with('"bar"')


class RemovePluginsCliTestCase(unittest.TestCase):
    def test_remove_plugins(self):
        term = MagicMock()
        args = Namespace(name=["foo", "bar"])

        existing = """[tool.autohooks]
mode = "pythonpath"
pre-commit = ["bar", "foo"]
"""
        expected = """[tool.autohooks]
mode = "pythonpath"
pre-commit = []
"""

        with temp_file(
            existing, name="pyproject.toml", change_into=True
        ) as pyproject_toml:
            remove_plugins(term, args)

            term.warning.assert_not_called()
            term.info.assert_has_calls([call("Removed plugins:")])
            term.ok.assert_has_calls([call('"bar"'), call('"foo"')])

            content = pyproject_toml.read_text(encoding="utf8")

            self.assertEqual(content, expected)

    def test_no_config(self):
        term = MagicMock()
        args = Namespace(name=["foo", "bar"])

        with tempdir(change_into=True) as temp_dir:
            remove_plugins(term, args)

            term.warning.assert_called_once_with("No plugins to remove.")
            term.info.assert_not_called()
            term.ok.assert_not_called()

            pyproject_toml = temp_dir / "pyproject.toml"
            self.assertFalse(pyproject_toml.exists())

    def test_remove_plugins_skipped(self):
        term = MagicMock()
        args = Namespace(name=["foo", "bar"])

        existing = """[tool.autohooks]
mode = "pythonpath"
pre-commit = ["foo"]
"""
        expected = """[tool.autohooks]
mode = "pythonpath"
pre-commit = []
"""

        with temp_file(
            existing, name="pyproject.toml", change_into=True
        ) as pyproject_toml:
            remove_plugins(term, args)

            term.warning.assert_called_once_with('"bar"')
            term.info.assert_has_calls(
                [
                    call("Skipped not used plugins:"),
                    call("Removed plugins:"),
                    call("Currently used plugins:"),
                ]
            )
            term.ok.assert_has_calls([call('"foo"')])

            content = pyproject_toml.read_text(encoding="utf8")

            self.assertEqual(content, expected)
