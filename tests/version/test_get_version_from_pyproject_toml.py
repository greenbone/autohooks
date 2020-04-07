# -*- coding: utf-8 -*-
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

from autohooks.version import get_version_from_pyproject_toml, VersionError


class GetVersionFromPyprojectTomlTestCase(unittest.TestCase):
    def test_pyproject_toml_file_not_exists(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.__str__.return_value = 'pyproject.toml'
        fake_path.exists.return_value = False

        with self.assertRaisesRegex(
            VersionError, 'pyproject.toml file not found'
        ):
            get_version_from_pyproject_toml(fake_path)

        fake_path.exists.assert_called_with()

    def test_no_poerty_section(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.__str__.return_value = 'pyproject.toml'
        fake_path.exists.return_value = True
        fake_path.read_text.return_value = ''

        with self.assertRaisesRegex(
            VersionError, 'Version information not found in pyproject.toml file'
        ):
            get_version_from_pyproject_toml(fake_path)

        fake_path.exists.assert_called_with()
        fake_path.read_text.assert_called_with()

    def test_empty_poerty_section(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.__str__.return_value = 'pyproject.toml'
        fake_path.exists.return_value = True
        fake_path.read_text.return_value = '[tool.poetry]'

        with self.assertRaisesRegex(
            VersionError, 'Version information not found in pyproject.toml file'
        ):
            get_version_from_pyproject_toml(fake_path)

        fake_path.exists.assert_called_with()
        fake_path.read_text.assert_called_with()

    def test_get_version(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value
        fake_path.__str__.return_value = 'pyproject.toml'
        fake_path.exists.return_value = True
        fake_path.read_text.return_value = '[tool.poetry]\nversion = "1.2.3"'

        version = get_version_from_pyproject_toml(fake_path)

        self.assertEqual(version, '1.2.3')

        fake_path.exists.assert_called_with()
        fake_path.read_text.assert_called_with()
