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
    get_pre_commit_hook_path,
    get_pre_commit_hook_template_path,
    install_pre_commit_hook,
)
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


class GetPreCommitHookTemplatePath(unittest.TestCase):
    def test_template_exists(self):
        template_path = get_pre_commit_hook_template_path()
        self.assertTrue(template_path.exists())
        self.assertTrue(template_path.is_file())


class InstallPreCommitHook(GitDirTestCase):
    def test_install(self):
        template_path = get_pre_commit_hook_template_path()
        pre_commmit_hook_path = get_pre_commit_hook_path()

        self.assertTrue(template_path.exists())
        self.assertFalse(pre_commmit_hook_path.exists())

        install_pre_commit_hook(template_path, pre_commmit_hook_path)

        self.assertTrue(pre_commmit_hook_path.exists())
