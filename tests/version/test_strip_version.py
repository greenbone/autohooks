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

from autohooks.version import strip_version


class StripVersionTestCase(unittest.TestCase):
    def test_version_string_without_v(self):
        self.assertEqual(strip_version('1.2.3'), '1.2.3')
        self.assertEqual(strip_version('1.2.3dev'), '1.2.3dev')

    def test_version_string_with_v(self):
        self.assertEqual(strip_version('v1.2.3'), '1.2.3')
        self.assertEqual(strip_version('v1.2.3dev'), '1.2.3dev')
