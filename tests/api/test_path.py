# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from pathlib import Path

from autohooks.api.git import StatusEntry
from autohooks.api.path import is_python_path, match


class MatchTestCase(unittest.TestCase):
    def test_match_list(self):
        patterns = ["*.py", "*.js"]

        self.assertTrue(match(Path("foo.py"), patterns))
        self.assertTrue(match(Path("foo.js"), patterns))
        self.assertTrue(match(Path("path/to/foo.py"), patterns))
        self.assertTrue(match(Path("/root/path/to/foo.py"), patterns))

        self.assertFalse(match(Path("foo.pyc"), patterns))
        self.assertFalse(match(Path("foo.c"), patterns))

    def test_match_tuple(self):
        patterns = ("*.py", "*.js")

        self.assertTrue(match(Path("foo.py"), patterns))
        self.assertTrue(match(Path("foo.js"), patterns))
        self.assertTrue(match(Path("path/to/foo.py"), patterns))
        self.assertTrue(match(Path("/root/path/to/foo.py"), patterns))

        self.assertFalse(match(Path("foo.pyc"), patterns))
        self.assertFalse(match(Path("foo.c"), patterns))

    def test_match_files_in_subdir(self):
        patterns = ("foo/*.py", "bar/*.js")

        self.assertFalse(match(Path("foo.py"), patterns))
        self.assertFalse(match(Path("foo.js"), patterns))
        self.assertFalse(match(Path("foo.pyc"), patterns))
        self.assertFalse(match(Path("foo.c"), patterns))

        self.assertTrue(match(Path("foo/bar.py"), patterns))
        self.assertTrue(match(Path("bar/foo.js"), patterns))

        self.assertFalse(match(Path("foo/bar.js"), patterns))
        self.assertFalse(match(Path("bar/foo.py"), patterns))

    def test_match_status_entry(self):
        patterns = ["*.py", "*.js"]

        self.assertTrue(match(StatusEntry("MM foo.py"), patterns))
        self.assertTrue(match(StatusEntry("MM foo.js"), patterns))
        self.assertTrue(match(StatusEntry("MM path/to/foo.py"), patterns))
        self.assertTrue(match(StatusEntry("MM /root/path/to/foo.py"), patterns))

        self.assertFalse(match(StatusEntry("MM foo.pyc"), patterns))
        self.assertFalse(match(StatusEntry("MM foo.c"), patterns))


class IsPythonPathTestCase(unittest.TestCase):
    def test_is_python_path(self):
        self.assertTrue(is_python_path(Path("foo.py")))
        self.assertTrue(is_python_path(Path("foo.bar.py")))
        self.assertTrue(is_python_path(Path("foo/bar/baz.py")))
        self.assertFalse(is_python_path(Path("foo/bar/baz.pyc")))
        self.assertFalse(is_python_path(Path("foo/bar/baz.py.txt")))
        self.assertFalse(is_python_path(Path("foo/bar/python.txt")))
        self.assertFalse(is_python_path(None))
        self.assertFalse(is_python_path(""))
        self.assertFalse(is_python_path(Path()))


if __name__ == "__main__":
    unittest.main()
