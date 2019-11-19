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

from autohooks.api.path import match


class MatchTestCase(unittest.TestCase):
    def test_match_list(self):
        patterns = ['*.py', '*.js']

        self.assertTrue(match(Path('foo.py'), patterns))
        self.assertTrue(match(Path('foo.js'), patterns))
        self.assertTrue(match(Path('path/to/foo.py'), patterns))
        self.assertTrue(match(Path('/root/path/to/foo.py'), patterns))

        self.assertFalse(match(Path('foo.pyc'), patterns))
        self.assertFalse(match(Path('foo.c'), patterns))

    def test_match_tuple(self):
        patterns = ('*.py', '*.js')

        self.assertTrue(match(Path('foo.py'), patterns))
        self.assertTrue(match(Path('foo.js'), patterns))
        self.assertTrue(match(Path('path/to/foo.py'), patterns))
        self.assertTrue(match(Path('/root/path/to/foo.py'), patterns))

        self.assertFalse(match(Path('foo.pyc'), patterns))
        self.assertFalse(match(Path('foo.c'), patterns))

    def test_match_files_in_subdir(self):
        patterns = ('foo/*.py', 'bar/*.js')

        self.assertFalse(match(Path('foo.py'), patterns))
        self.assertFalse(match(Path('foo.js'), patterns))
        self.assertFalse(match(Path('foo.pyc'), patterns))
        self.assertFalse(match(Path('foo.c'), patterns))

        self.assertTrue(match(Path('foo/bar.py'), patterns))
        self.assertTrue(match(Path('bar/foo.js'), patterns))

        self.assertFalse(match(Path('foo/bar.js'), patterns))
        self.assertFalse(match(Path('bar/foo.py'), patterns))


if __name__ == '__main__':
    unittest.main()
