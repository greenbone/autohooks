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

import unittest
from pathlib import Path

from autohooks.api.git import (
    Status,
    StatusEntry,
    get_status,
    is_partially_staged_status,
    is_staged_status,
)

from . import GitTestCase, git_add, git_commit, git_mv, git_rm, tempgitdir


def init_test_repo(tmpdir: Path):
    tracked_file = tmpdir / "foo.json"
    tracked_file.write_text("sed diam nonumy eirmod")
    changed_file = tmpdir / "bar.json"
    changed_file.touch()
    staged_changed_file = tmpdir / "ipsum.json"
    staged_changed_file.write_text("tempor invidunt ut labore")
    removed_file = tmpdir / "lorem.json"
    removed_file.write_text("consetetur sadipscing elitr")
    renamed_file = tmpdir / "foo.md"
    renamed_file.write_text("et dolore magna aliquyam erat")

    git_add(
        tracked_file,
        changed_file,
        staged_changed_file,
        removed_file,
        renamed_file,
    )
    git_commit()

    changed_file.write_text("Lorem Ipsum")
    staged_changed_file.write_text("Lorem Ipsum")

    added_file = tmpdir / "foo.txt"
    added_file.touch()

    added_modified_file = tmpdir / "ipsum.txt"
    added_modified_file.touch()

    git_add(added_file, staged_changed_file, added_modified_file)

    staged_changed_file.write_text("Dolor sit")

    added_modified_file.write_text("Lorem Ipsum")

    git_mv(renamed_file, tmpdir / "foo.rst")

    git_rm(removed_file)

    untracked_file = tmpdir / "bar.txt"
    untracked_file.touch()

    return (
        tracked_file,
        changed_file,
        added_file,
        staged_changed_file,
        added_modified_file,
        removed_file,
        renamed_file,
        untracked_file,
    )


class StatusEntryTestCase(unittest.TestCase):
    def test_parse_modified_modified(self):
        status = StatusEntry("MM foo.txt")

        self.assertEqual(status.index, Status.MODIFIED)
        self.assertEqual(status.working_tree, Status.MODIFIED)
        self.assertEqual(status.path, Path("foo.txt"))

    def test_parse_modified_unmodified(self):
        status = StatusEntry("M  foo.txt")

        self.assertEqual(status.index, Status.MODIFIED)
        self.assertEqual(status.working_tree, Status.UNMODIFIED)
        self.assertEqual(status.path, Path("foo.txt"))

    def test_parse_deleted(self):
        status = StatusEntry("D  foo.txt")

        self.assertEqual(status.index, Status.DELETED)
        self.assertEqual(status.working_tree, Status.UNMODIFIED)
        self.assertEqual(status.path, Path("foo.txt"))

    def test_parse_added(self):
        status = StatusEntry("A  foo.txt")

        self.assertEqual(status.index, Status.ADDED)
        self.assertEqual(status.working_tree, Status.UNMODIFIED)
        self.assertEqual(status.path, Path("foo.txt"))

    def test_parse_untracked(self):
        status = StatusEntry("?? foo.txt")

        self.assertEqual(status.index, Status.UNTRACKED)
        self.assertEqual(status.working_tree, Status.UNTRACKED)
        self.assertEqual(status.path, Path("foo.txt"))

    def test_parse_ignored_untracked(self):
        status = StatusEntry("!? foo.txt")

        self.assertEqual(status.index, Status.IGNORED)
        self.assertEqual(status.working_tree, Status.UNTRACKED)
        self.assertEqual(status.path, Path("foo.txt"))


class GetStatusTestCase(GitTestCase):
    def test_get_status(self):
        with tempgitdir() as tmpdir:
            (
                _tracked_file,
                changed_file,
                added_file,
                staged_changed_file,
                added_modifed_file,
                removed_file,
                renamed_file,
                _untracked_file,
            ) = init_test_repo(tmpdir)

            status = get_status()
            self.assertEqual(len(status), 6)

            changed_file_status = status[0]
            renamed_file_status = status[1]
            added_file_status = status[2]
            staged_changed_file_status = status[3]
            added_modifed_file_status = status[4]
            removed_file_status = status[5]

            self.assertEqual(changed_file_status.absolute_path(), changed_file)
            self.assertEqual(changed_file_status.index, Status.UNMODIFIED)
            self.assertEqual(changed_file_status.working_tree, Status.MODIFIED)

            self.assertEqual(
                renamed_file_status.old_path.absolute(), renamed_file
            )
            self.assertEqual(renamed_file_status.index, Status.RENAMED)
            self.assertEqual(
                renamed_file_status.working_tree, Status.UNMODIFIED
            )

            self.assertEqual(added_file_status.absolute_path(), added_file)
            self.assertEqual(added_file_status.index, Status.ADDED)
            self.assertEqual(added_file_status.working_tree, Status.UNMODIFIED)

            self.assertEqual(
                staged_changed_file_status.absolute_path(), staged_changed_file
            )
            self.assertEqual(staged_changed_file_status.index, Status.MODIFIED)
            self.assertEqual(
                staged_changed_file_status.working_tree, Status.MODIFIED
            )

            self.assertEqual(
                added_modifed_file_status.absolute_path(), added_modifed_file
            )
            self.assertEqual(added_modifed_file_status.index, Status.ADDED)
            self.assertEqual(
                added_modifed_file_status.working_tree, Status.MODIFIED
            )

            self.assertEqual(removed_file_status.absolute_path(), removed_file)
            self.assertEqual(removed_file_status.index, Status.DELETED)
            self.assertEqual(
                removed_file_status.working_tree, Status.UNMODIFIED
            )

    def test_get_status_for_files(self):
        with tempgitdir() as tmpdir:
            (
                _tracked_file,
                changed_file,
                _added_file,
                _staged_changed_file,
                _added_modifed_file,
                _removed_file,
                renamed_file,
                _untracked_file,
            ) = init_test_repo(tmpdir)

            status = get_status((changed_file, renamed_file))

            self.assertEqual(len(status), 2)

            changed_file_status = status[0]
            renamed_file_status = status[1]

            self.assertEqual(changed_file_status.absolute_path(), changed_file)
            self.assertEqual(changed_file_status.index, Status.UNMODIFIED)
            self.assertEqual(changed_file_status.working_tree, Status.MODIFIED)

            # the status is deleted for the renamed file because the new file
            # path is not passed to get_status
            self.assertEqual(renamed_file_status.absolute_path(), renamed_file)
            self.assertEqual(renamed_file_status.index, Status.DELETED)
            self.assertEqual(
                renamed_file_status.working_tree, Status.UNMODIFIED
            )

    def test_is_staged_status(self):
        with tempgitdir() as tmpdir:
            init_test_repo(tmpdir)

            status = get_status()

            changed_file_status = status[0]
            renamed_file_status = status[1]
            added_file_status = status[2]
            staged_changed_file_status = status[3]
            added_modifed_file_status = status[4]
            removed_file_status = status[5]

            self.assertFalse(is_staged_status(changed_file_status))
            self.assertTrue(is_staged_status(renamed_file_status))
            self.assertTrue(is_staged_status(added_file_status))
            self.assertTrue(is_staged_status(staged_changed_file_status))
            self.assertTrue(is_staged_status(added_modifed_file_status))
            self.assertFalse(is_staged_status(removed_file_status))

    def test_is_partially_staged_status(self):
        with tempgitdir() as tmpdir:
            init_test_repo(tmpdir)

            status = get_status()

            changed_file_status = status[0]
            renamed_file_status = status[1]
            added_file_status = status[2]
            staged_changed_file_status = status[3]
            added_modifed_file_status = status[4]
            removed_file_status = status[5]

            self.assertFalse(is_partially_staged_status(changed_file_status))
            self.assertFalse(is_partially_staged_status(renamed_file_status))
            self.assertFalse(is_partially_staged_status(added_file_status))
            self.assertTrue(
                is_partially_staged_status(staged_changed_file_status)
            )
            self.assertTrue(
                is_partially_staged_status(added_modifed_file_status)
            )
            self.assertFalse(is_partially_staged_status(removed_file_status))
