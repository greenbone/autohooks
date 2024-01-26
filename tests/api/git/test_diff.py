# SPDX-FileCopyrightText: 2022-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
