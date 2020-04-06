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

from autohooks.version import VersionCommand


class UpdateVersionFileTestCase(unittest.TestCase):
    def test_update_version_file(self):
        fake_path_class = MagicMock(spec=Path)
        fake_path = fake_path_class.return_value

        cmd = VersionCommand(version_file_path=fake_path)
        cmd.update_version_file('22.04dev1')

        text = fake_path.write_text.call_args[0][0]

        *_, version_line, _last_line = text.split('\n')

        self.assertEqual(version_line, '__version__ = "22.4.dev1"')
