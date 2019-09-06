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

import os
import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from autohooks.install import (
    get_autohooks_pre_commit_hook,
    get_pre_commit_hook_path,
    install_pre_commit_hook,
    is_autohooks_pre_commit_hook,
)
from autohooks.setting import Mode
from autohooks.template import get_pre_commit_hook_template_path
from autohooks.utils import exec_git


class GitDirTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.temp_dir_path = Path(self.tempdir.name)

        exec_git('-C', str(self.temp_dir_path), 'init')

        self.git_dir_path = self.temp_dir_path / '.git'

        self.assertTrue(self.git_dir_path.exists())

        os.environ['PWD'] = str(self.temp_dir_path)

    def tearDown(self):
        self.tempdir.cleanup()


class GetPreCommitHookPathTestCase(GitDirTestCase):
    def test_get_path(self):
        pre_commmit_hook_path = get_pre_commit_hook_path()

        self.assertEqual(
            pre_commmit_hook_path,
            self.temp_dir_path / '.git' / 'hooks' / 'pre-commit',
        )


class InstallPreCommitHook(GitDirTestCase):
    def test_install(self):
        hooks = get_autohooks_pre_commit_hook(mode=Mode.PIPENV)
        pre_commmit_hook_path = get_pre_commit_hook_path()

        self.assertFalse(pre_commmit_hook_path.exists())

        install_pre_commit_hook(hooks, pre_commmit_hook_path)

        self.assertTrue(pre_commmit_hook_path.exists())


class FakeHookPath:
    def __init__(self, text):
        self._text = text

    def read_text(self):
        return self._text


class IsAutohooksPreCommitHook(unittest.TestCase):
    def test_other_hook(self):
        path = FakeHookPath('foo\nbar')
        self.assertFalse(is_autohooks_pre_commit_hook(path))

    def test_pre_commit_template_path(self):
        path = get_pre_commit_hook_template_path()
        self.assertTrue(is_autohooks_pre_commit_hook(path))


if __name__ == '__main__':
    unittest.main()
