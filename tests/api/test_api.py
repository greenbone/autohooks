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

from autohooks.config import load_config_from_pyproject_toml
from autohooks.api import get_company


def get_test_config_path(name):
    return Path(__file__).parent.parent / name


class GetCompanyTestCase(unittest.TestCase):
    def test_with_config_file(self):
        config_path = get_test_config_path('pyproject.test1.toml')
        self.assertTrue(config_path.is_file())

        config = load_config_from_pyproject_toml(config_path)

        company = get_company(config=config)
        self.assertEqual('Greenbone', company.get_value())

        config_path = get_test_config_path('pyproject.test2.toml')
        self.assertTrue(config_path.is_file())

        config = load_config_from_pyproject_toml(config_path)

        company = get_company(config=config)
        self.assertEqual('glurp', company.get_value())
