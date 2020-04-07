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

from autohooks.version import safe_version


class SafeVersionTestCase(unittest.TestCase):
    def test_dev_versions(self):
        self.assertEqual(safe_version('1.2.3dev'), '1.2.3.dev0')
        self.assertEqual(safe_version('1.2.3dev1'), '1.2.3.dev1')
        self.assertEqual(safe_version('1.2.3.dev'), '1.2.3.dev0')

    def test_alpha_versions(self):
        self.assertEqual(safe_version('1.2.3alpha'), '1.2.3a0')
        self.assertEqual(safe_version('1.2.3.alpha'), '1.2.3a0')
        self.assertEqual(safe_version('1.2.3a'), '1.2.3a0')
        self.assertEqual(safe_version('1.2.3.a1'), '1.2.3a1')
        self.assertEqual(safe_version('1.2.3a1'), '1.2.3a1')

    def test_beta_versions(self):
        self.assertEqual(safe_version('1.2.3beta'), '1.2.3b0')
        self.assertEqual(safe_version('1.2.3.beta'), '1.2.3b0')
        self.assertEqual(safe_version('1.2.3b'), '1.2.3b0')
        self.assertEqual(safe_version('1.2.3.b1'), '1.2.3b1')
        self.assertEqual(safe_version('1.2.3b1'), '1.2.3b1')

    def test_caldav_versions(self):
        self.assertEqual(safe_version('22.04'), '22.4')
        self.assertEqual(safe_version('22.4'), '22.4')
        self.assertEqual(safe_version('22.10'), '22.10')
        self.assertEqual(safe_version('22.04dev1'), '22.4.dev1')
        self.assertEqual(safe_version('22.10dev1'), '22.10.dev1')

    def test_release_versions(self):
        self.assertEqual(safe_version('1'), '1')
        self.assertEqual(safe_version('1.2'), '1.2')
        self.assertEqual(safe_version('1.2.3'), '1.2.3')
        self.assertEqual(safe_version('22.4'), '22.4')
