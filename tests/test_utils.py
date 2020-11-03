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

from autohooks.utils import (
    exec_git,
    get_git_hook_directory_path,
    is_project_root,
    get_project_root_path,
    get_project_autohooks_plugins_path,
    get_pyproject_toml_path,
    get_git_directory_path,
)


class GitHookDirPathTestCase(unittest.TestCase):
    def test_get_git_hook_directory_path(self):
        path = Path('foo')
        git_hook_dir_path = get_git_hook_directory_path(path)
        self.assertEqual(git_hook_dir_path, path / 'hooks')

    def test_with_env_pwd(self):
        with TemporaryDirectory() as f:
            temp_path = Path(f)

            exec_git('-C', str(temp_path), 'init')

            os.environ['PWD'] = str(temp_path)

            git_dir_path = (temp_path / '.git').resolve()

            git_hook_dir_path = get_git_hook_directory_path()
            self.assertEqual(git_hook_dir_path, git_dir_path / 'hooks')


class IsProjectRootTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.temp_path = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_no_root(self):
        self.assertFalse(is_project_root(self.temp_path))

    def test_pyproject_toml(self):
        pyproject_toml = self.temp_path / 'pyproject.toml'
        pyproject_toml.touch()

        self.assertTrue(pyproject_toml.exists())
        self.assertTrue(is_project_root(self.temp_path))

    def test_dot_git(self):
        git_dir = self.temp_path / '.git'
        git_dir.mkdir()

        self.assertTrue(git_dir.exists())
        self.assertTrue(git_dir.is_dir())
        self.assertTrue(is_project_root(self.temp_path))

    def test_setup_py(self):
        setup_py = self.temp_path / 'setup.py'
        setup_py.touch()

        self.assertTrue(setup_py.exists())
        self.assertTrue(is_project_root(self.temp_path))

    def test_setup_cfg(self):
        setup_cfg = self.temp_path / 'setup.cfg'
        setup_cfg.touch()

        self.assertTrue(setup_cfg.exists())
        self.assertTrue(is_project_root(self.temp_path))


class GetProjectRootPath(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.temp_path = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_direct_root(self):
        setup_py = self.temp_path / 'setup.py'
        setup_py.touch()

        root_path = get_project_root_path(self.temp_path)

        self.assertEqual(root_path, self.temp_path)

    def test_with_sub_directory(self):
        sub_path = self.temp_path / 'foo'
        sub_path.mkdir()
        setup_py = self.temp_path / 'setup.py'
        setup_py.touch()

        root_path = get_project_root_path(sub_path)

        self.assertEqual(root_path, self.temp_path)

    def test_without_project_root(self):
        root_path = get_project_root_path(self.temp_path)

        self.assertEqual(root_path, self.temp_path)

    def test_with_env_pwd(self):
        setup_py = self.temp_path / 'setup.py'
        setup_py.touch()
        sub_path = self.temp_path / 'foo'
        sub_path.mkdir()

        os.environ['PWD'] = str(sub_path)

        root_path = get_project_root_path()

        self.assertEqual(root_path, self.temp_path)


class GetProjectAutohooksPluginsPathTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.temp_path = Path(self.tempdir.name)

        setup_py = self.temp_path / 'setup.py'
        setup_py.touch()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_with_subpath(self):
        sub_path = self.temp_path / 'foo'
        sub_path.mkdir()

        autohooks_plugins_path = get_project_autohooks_plugins_path(sub_path)
        self.assertEqual(autohooks_plugins_path, self.temp_path / '.autohooks')

    def test_with_env_pwd(self):
        os.environ['PWD'] = str(self.temp_path)

        autohooks_plugins_path = get_project_autohooks_plugins_path()
        self.assertEqual(autohooks_plugins_path, self.temp_path / '.autohooks')


class GetPyProjectTomlPathTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.temp_path = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_with_pyproject_toml_file(self):
        pyproject_toml_file = self.temp_path / 'pyproject.toml'
        pyproject_toml_file.touch()

        sub_path = self.temp_path / 'foo'
        sub_path.mkdir()

        pyproject_toml_path = get_pyproject_toml_path(sub_path)
        self.assertEqual(pyproject_toml_path, self.temp_path / 'pyproject.toml')

    def test_with_env_pwd(self):
        os.environ['PWD'] = str(self.temp_path)

        setup_py = self.temp_path / 'setup.py'
        setup_py.touch()

        pyproject_toml_path = get_pyproject_toml_path()
        self.assertEqual(pyproject_toml_path, self.temp_path / 'pyproject.toml')


class GetGitDirectoryPath(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.temp_path = Path(self.tempdir.name)

        exec_git('-C', str(self.temp_path), 'init')

        self.git_dir_path = (self.temp_path / '.git').resolve()

        self.assertTrue(self.git_dir_path.exists())

    def tearDown(self):
        self.tempdir.cleanup()

    def test_with_root_dir(self):
        os.environ['PWD'] = str(self.temp_path)

        git_dir_path = get_git_directory_path()
        self.assertEqual(git_dir_path, self.git_dir_path.resolve())

    def test_with_subdir(self):
        sub_path = self.temp_path / 'foo'
        sub_path.mkdir()

        os.environ['PWD'] = str(sub_path)

        git_dir_path = get_git_directory_path()
        self.assertEqual(git_dir_path, self.git_dir_path)


if __name__ == '__main__':
    unittest.main()
