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

from autohooks.api.git import Status, get_status, stash_unstaged_changes
from tests import tempgitdir

from . import GitTestCase, git_add, randbytes


class StashUnstagedChangesTestCase(GitTestCase):
    def test_no_working_files(self):
        with tempgitdir() as tmpdir:
            file1 = tmpdir / "foo.txt"
            file1.write_bytes(randbytes(20))

            git_add(file1)

            stash = stash_unstaged_changes()
            with stash:
                self.assertEqual(len(stash.partially_staged), 0)

    def test_staged_with_working_files(self):
        with tempgitdir() as tmpdir:
            file1 = tmpdir / "foo.txt"
            file1.write_bytes(randbytes(20))

            git_add(file1)

            file1 = tmpdir / "bar.txt"
            file1.write_bytes(randbytes(20))

            stash = stash_unstaged_changes()
            with stash:
                self.assertEqual(len(stash.partially_staged), 0)

    def test_partiall_staged_files(self):
        with tempgitdir() as tmpdir:
            file1 = tmpdir / "foo.txt"
            file1.write_bytes(randbytes(20))

            git_add(file1)

            file1.write_bytes(randbytes(20))

            status = get_status()
            self.assertEqual(status[0].index, Status.ADDED)
            self.assertEqual(status[0].working_tree, Status.MODIFIED)

            stash = stash_unstaged_changes()
            with stash:
                self.assertEqual(len(stash.partially_staged), 1)

                status = get_status()
                self.assertEqual(status[0].index, Status.ADDED)
                self.assertEqual(status[0].working_tree, Status.UNMODIFIED)

            status = get_status()
            self.assertEqual(status[0].index, Status.ADDED)
            self.assertEqual(status[0].working_tree, Status.MODIFIED)

    def test_partiall_staged_files_with_error(self):
        with tempgitdir() as tmpdir:
            file1 = tmpdir / "foo.txt"
            file1.write_bytes(randbytes(20))

            git_add(file1)

            content = randbytes(20)
            file1.write_bytes(content)

            status = get_status()
            self.assertEqual(status[0].index, Status.ADDED)
            self.assertEqual(status[0].working_tree, Status.MODIFIED)

            stash = stash_unstaged_changes()

            with self.assertRaises(ValueError):
                with stash:
                    self.assertEqual(len(stash.partially_staged), 1)

                    status = get_status()
                    self.assertEqual(status[0].index, Status.ADDED)
                    self.assertEqual(status[0].working_tree, Status.UNMODIFIED)

                    raise ValueError("An error ocurred!")

            status = get_status()
            self.assertEqual(status[0].index, Status.ADDED)
            self.assertEqual(status[0].working_tree, Status.MODIFIED)

            self.assertEqual(content, file1.read_bytes())

    def test_partiall_staged_files_with_error_and_changed_content(self):
        with tempgitdir() as tmpdir:
            file1 = tmpdir / "foo.txt"
            file1.write_bytes(randbytes(20))

            git_add(file1)

            content = randbytes(20)
            file1.write_bytes(content)

            status = get_status()
            self.assertEqual(status[0].index, Status.ADDED)
            self.assertEqual(status[0].working_tree, Status.MODIFIED)

            stash = stash_unstaged_changes()

            with self.assertRaises(ValueError):
                with stash:
                    self.assertEqual(len(stash.partially_staged), 1)

                    status = get_status()
                    self.assertEqual(status[0].index, Status.ADDED)
                    self.assertEqual(status[0].working_tree, Status.UNMODIFIED)

                    content2 = randbytes(20)
                    file1.write_bytes(content2)

                    raise ValueError("An error ocurred!")

            status = get_status()
            self.assertEqual(status[0].index, Status.ADDED)
            self.assertEqual(status[0].working_tree, Status.MODIFIED)

            self.assertEqual(content, file1.read_bytes())

    def test_formatting_plugin_with_untracked_change(self):
        with tempgitdir() as tmpdir:
            content = "Lorem Ipsum"
            content2 = "Lorem Ipsum\nDolor Sit"
            content3 = "Lorem Ipsum\nDolor Sit\namet consetetur sadipscing"

            file1 = tmpdir / "foo.txt"
            file1.write_text(content, encoding="utf8")

            git_add(file1)

            file1.write_text(content2, encoding="utf8")

            stash = stash_unstaged_changes()
            with stash:
                self.assertEqual(len(stash.partially_staged), 1)
                self.assertEqual(content, file1.read_text(encoding="utf8"))

                file1.write_text(content3, encoding="utf8")

            self.assertEqual(content2, file1.read_text(encoding="utf8"))

    def test_formatting_plugin_with_staged_change(self):
        with tempgitdir() as tmpdir:
            content = "Lorem Ipsum"
            content2 = "Lorem Ipsum\nDolor Sit"

            file1 = tmpdir / "foo.txt"
            file1.write_text(content, encoding="utf8")

            git_add(file1)

            file1.write_text(content2, encoding="utf8")

            stash = stash_unstaged_changes()
            with stash:
                self.assertEqual(len(stash.partially_staged), 1)
                self.assertEqual(content, file1.read_text(encoding="utf8"))

                file1.write_text(content2, encoding="utf8")

                git_add(file1)

            self.assertEqual(content2, file1.read_text(encoding="utf8"))

    def test_formatting_plugin_with_conflicting_staged_change(self):
        with tempgitdir() as tmpdir:
            content = "Lorem Ipsum\n\n\n"
            content2 = "Lorem Ipsum\nDolor Sit\n\n"
            content3 = "Lorem Ipsum\n\nAmet\n"
            content4 = "Lorem Ipsum\nDolor Sit\nAmet\n"

            file1 = tmpdir / "foo.txt"
            file1.write_text(content, encoding="utf8")

            git_add(file1)

            file1.write_text(content2, encoding="utf8")

            stash = stash_unstaged_changes()
            with stash:
                self.assertEqual(len(stash.partially_staged), 1)
                self.assertEqual(content, file1.read_text(encoding="utf8"))

                file1.write_text(content3, encoding="utf8")

                git_add(file1)

            self.assertEqual(content4, file1.read_text(encoding="utf8"))
