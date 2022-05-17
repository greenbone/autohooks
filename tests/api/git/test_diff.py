# Copyright (C) 2022 Greenbone Networks GmbH
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

from autohooks.api.git import StatusEntry, get_diff
from tests import tempgitdir
from tests.api.git import GitTestCase, git_add, git_commit


class DiffTestCase(GitTestCase):
    def test_get_diff_from_status(self):
        with tempgitdir() as tmpdir:
            test_file = tmpdir / "foo.txt"
            test_file.write_text(
                "Lorem\nipsum\ndolor\nsit\namet", encoding="utf8"
            )

            git_add(test_file)
            git_commit()

            test_file.write_text("ipsum\ndolor\nsit\namet", encoding="utf8")
            status = StatusEntry("M  foo.txt", tmpdir)
            diff = get_diff((status,))

            expected_diff = """--- a/foo.txt
+++ b/foo.txt
@@ -1,4 +1,3 @@
-Lorem
 ipsum
 dolor
 sit"""
            self.assertIn(expected_diff, diff)

    def test_get_diff(self):
        with tempgitdir() as tmpdir:
            test_file = tmpdir / "foo.txt"
            test_file.write_text(
                "Lorem\nipsum\ndolor\nsit\namet", encoding="utf8"
            )

            git_add(test_file)
            git_commit()

            test_file.write_text("ipsum\ndolor\nsit\namet", encoding="utf8")
            diff = get_diff()

            expected_diff = """--- a/foo.txt
+++ b/foo.txt
@@ -1,4 +1,3 @@
-Lorem
 ipsum
 dolor
 sit"""
            self.assertIn(expected_diff, diff)
