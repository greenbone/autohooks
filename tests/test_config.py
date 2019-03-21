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

import unittest

from pathlib import Path

from autohooks.config import load_config_from_pyproject_toml


class ConfigTestCase(unittest.TestCase):
    def test_load_from_toml_file(self):
        config_path = Path(__file__).parent / 'pyproject.test1.toml'
        self.assertTrue(config_path.is_file())

        config = load_config_from_pyproject_toml(config_path)

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())

        self.assertListEqual(
            config.get_pre_commit_script_names(), ['foo', 'bar']
        )
