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

from autohooks.version import AutohooksVersionCommand
from autohooks.__version__ import __version__ as current_version


class AutohooksVersionCommandTestCase(unittest.TestCase):
    def test_get_current_version(self):
        cmd = AutohooksVersionCommand()
        self.assertEqual(cmd.get_current_version(), current_version)

    def test_name(self):
        cmd = AutohooksVersionCommand()
        self.assertEqual(cmd.name, 'autohooks')

    def test_version_file_path(self):
        cmd = AutohooksVersionCommand()
        self.assertRegex(
            str(cmd.version_file_path), '^.*/autohooks/__version__.py$'
        )

    def test_pyproject_toml_path(self):
        cmd = AutohooksVersionCommand()
        self.assertRegex(str(cmd.pyproject_toml_path), '^.*/pyproject.toml$')
