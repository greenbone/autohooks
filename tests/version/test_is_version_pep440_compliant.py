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

from autohooks.version import is_version_pep440_compliant


class IsVersionPep440CompliantTestCase(unittest.TestCase):
    def test_is_compliant(self):
        self.assertTrue(is_version_pep440_compliant('1.2.3.dev1'))
        self.assertTrue(is_version_pep440_compliant('1.2.3.dev0'))
        self.assertTrue(is_version_pep440_compliant('20.4'))
        self.assertTrue(is_version_pep440_compliant('1.2'))
        self.assertTrue(is_version_pep440_compliant('1.2.0a0'))
        self.assertTrue(is_version_pep440_compliant('1.2.0a1'))
        self.assertTrue(is_version_pep440_compliant('1.2.0b0'))
        self.assertTrue(is_version_pep440_compliant('1.2.0b1'))

    def test_is_not_compliant(self):
        self.assertFalse(is_version_pep440_compliant('1.2.3dev1'))
        self.assertFalse(is_version_pep440_compliant('1.2.3dev'))
        self.assertFalse(is_version_pep440_compliant('1.2.3dev0'))
        self.assertFalse(is_version_pep440_compliant('1.2.3alpha'))
        self.assertFalse(is_version_pep440_compliant('1.2.3alpha0'))
        self.assertFalse(is_version_pep440_compliant('1.2.3.a0'))
        self.assertFalse(is_version_pep440_compliant('1.2.3beta'))
        self.assertFalse(is_version_pep440_compliant('1.2.3beta0'))
        self.assertFalse(is_version_pep440_compliant('1.2.3.b0'))
        self.assertFalse(is_version_pep440_compliant('20.04'))
