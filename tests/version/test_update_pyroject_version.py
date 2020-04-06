# Copyright (C) 2020 Greenbone Networks GmbH
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

from pathlib import Path
from unittest.mock import MagicMock

import tomlkit

from autohooks.version import VersionCommand


class UpdatePyprojectVersionTestCase(unittest.TestCase):
    def test_empty_pyproject_toml(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.read_text.return_value = ""

        cmd = VersionCommand(pyproject_toml_path=fake_path)

        cmd.update_pyproject_version('20.04dev1')

        text = fake_path.write_text.call_args[0][0]

        toml = tomlkit.parse(text)

        self.assertEqual(toml['tool']['poetry']['version'], '20.4.dev1')

    def test_empty_tool_section(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.read_text.return_value = "[tool]"

        cmd = VersionCommand(pyproject_toml_path=fake_path)
        cmd.update_pyproject_version('20.04dev1')

        text = fake_path.write_text.call_args[0][0]

        toml = tomlkit.parse(text)

        self.assertEqual(toml['tool']['poetry']['version'], '20.4.dev1')

    def test_empty_tool_poetry_section(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.read_text.return_value = "[tool.poetry]"

        cmd = VersionCommand(pyproject_toml_path=fake_path)
        cmd.update_pyproject_version('20.04dev1')

        text = fake_path.write_text.call_args[0][0]

        toml = tomlkit.parse(text)

        self.assertEqual(toml['tool']['poetry']['version'], '20.4.dev1')

    def test_override_existing_version(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.read_text.return_value = '[tool.poetry]\nversion = "1.2.3"'

        cmd = VersionCommand(pyproject_toml_path=fake_path)
        cmd.update_pyproject_version('20.04dev1')

        text = fake_path.write_text.call_args[0][0]

        toml = tomlkit.parse(text)

        self.assertEqual(toml['tool']['poetry']['version'], '20.4.dev1')
