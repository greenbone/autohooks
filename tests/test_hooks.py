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
import tempfile
import unittest

from unittest.mock import Mock

from pathlib import Path
from tempfile import TemporaryDirectory

from autohooks.hooks import PreCommitHook, get_pre_commit_hook_path
from autohooks.settings import Mode
from autohooks.template import (
    PreCommitTemplate,
    PIPENV_SHEBANG,
    POETRY_SHEBANG,
    PIPENV_MULTILINE_SHEBANG,
    POETRY_MULTILINE_SHEBANG,
    PYTHON3_SHEBANG,
    TEMPLATE_VERSION,
)
from autohooks.utils import exec_git


class GitDirTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.temp_dir_path = Path(self.tempdir.name).resolve()

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
        pre_commit_hook = PreCommitHook()

        self.assertFalse(pre_commit_hook.exists())

        pre_commit_hook.write(mode=Mode.PIPENV)

        self.assertTrue(pre_commit_hook.exists())


class FakeReadPath:
    def __init__(self, text):
        self._text = text

    def read_text(self):
        return self._text


class IsAutohooksPreCommitHook(unittest.TestCase):
    def test_other_hook(self):
        path = FakeReadPath('foo\nbar')
        pre_commit_hook = PreCommitHook(path)

        self.assertFalse(pre_commit_hook.is_autohooks_pre_commit_hook())

    def test_pre_commit_template(self):
        template = PreCommitTemplate()
        path = FakeReadPath(template.render(mode=Mode.PIPENV))
        pre_commit_hook = PreCommitHook(path)

        self.assertTrue(pre_commit_hook.is_autohooks_pre_commit_hook())


class IsCurrentAutohooksPreCommitHook(unittest.TestCase):
    def test_other_hook(self):
        path = FakeReadPath('foo\nbar')
        pre_commit_hook = PreCommitHook(path)

        self.assertFalse(pre_commit_hook.is_current_autohooks_pre_commit_hook())

    def test_pre_commit_template(self):
        template = PreCommitTemplate()
        path = FakeReadPath(template.render(mode=Mode.PIPENV))
        pre_commit_hook = PreCommitHook(path)

        self.assertTrue(pre_commit_hook.is_current_autohooks_pre_commit_hook())

    def test_modified_pre_commit_template(self):
        template = PreCommitTemplate()
        rendered = template.render(mode=Mode.PIPENV)
        lines = rendered.split('\n')
        lines[1] = ""
        path = FakeReadPath("\n".join(lines))
        pre_commit_hook = PreCommitHook(path)

        self.assertFalse(pre_commit_hook.is_current_autohooks_pre_commit_hook())


class ReadVersionTestCase(unittest.TestCase):
    def test_read_version(self):
        template = PreCommitTemplate()
        with tempfile.TemporaryDirectory() as tempdir:
            tmp_hook_path = Path(tempdir) / 'pre-commit-test'
            # Find version using all shebang modes
            for mode in [m for m in Mode if m.value > 0]:
                with open(str(tmp_hook_path), 'w') as tmpfile:
                    tmpfile.write(template.render(mode=mode))
                pre_commit_hook = PreCommitHook(tmp_hook_path)

            self.assertEqual(TEMPLATE_VERSION, pre_commit_hook.read_version())

    def test_empty_content(self):
        path = FakeReadPath("")
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_version(), -1)

    def test_no_meta(self):
        path = FakeReadPath("\n# foo = bar")
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_version(), -1)


class ReadModeTestCase(unittest.TestCase):
    def test_undefined_mode(self):
        path = FakeReadPath("")
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_mode(), Mode.UNDEFINED)

    def test_unknown_mode(self):
        path = FakeReadPath("#!foo")
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_mode(), Mode.UNKNOWN)

    def test_pipenv_mode(self):
        path = FakeReadPath("#!{}".format(PIPENV_SHEBANG))
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_mode(), Mode.PIPENV)

    def test_poetry_mode(self):
        path = FakeReadPath("#!{}".format(POETRY_SHEBANG))
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_mode(), Mode.POETRY)

    def test_pipenv_multiline_mode(self):
        path = FakeReadPath("#!{}".format(PIPENV_MULTILINE_SHEBANG))
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_mode(), Mode.PIPENV_MULTILINE)

    def test_poetry_multiline_mode(self):
        path = FakeReadPath("#!{}".format(POETRY_MULTILINE_SHEBANG))
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_mode(), Mode.POETRY_MULTILINE)

    def test_pythonpath_mode(self):
        path = FakeReadPath("#!{}".format(PYTHON3_SHEBANG))
        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(pre_commit_hook.read_mode(), Mode.PYTHONPATH)


class WriteTestCase(unittest.TestCase):
    def test_pipenv_mode(self):
        write_path = Mock()
        pre_commit_hook = PreCommitHook(write_path)
        pre_commit_hook.write(mode=Mode.PIPENV)

        write_path.chmod.assert_called_with(0o775)
        self.assertTrue(write_path.write_text.called)

        args, _kwargs = write_path.write_text.call_args
        text = args[0]
        self.assertRegex(text, '^#!{} *'.format(PIPENV_SHEBANG))

    def test_poetry_mode(self):
        write_path = Mock()
        pre_commit_hook = PreCommitHook(write_path)
        pre_commit_hook.write(mode=Mode.POETRY)

        write_path.chmod.assert_called_with(0o775)
        self.assertTrue(write_path.write_text.called)

        args, _kwargs = write_path.write_text.call_args
        text = args[0]
        self.assertRegex(text, '^#!{} *'.format(POETRY_SHEBANG))

    def test_pythonpath_mode(self):
        write_path = Mock()
        pre_commit_hook = PreCommitHook(write_path)
        pre_commit_hook.write(mode=Mode.PYTHONPATH)

        write_path.chmod.assert_called_with(0o775)
        self.assertTrue(write_path.write_text.called)

        args, _kwargs = write_path.write_text.call_args
        text = args[0]
        self.assertRegex(text, '^#!{} *'.format(PYTHON3_SHEBANG))


class StrTestCase(unittest.TestCase):
    def test_str_conversion(self):
        path = Mock()
        path.__str__ = Mock(return_value="foo")

        pre_commit_hook = PreCommitHook(path)

        self.assertEqual(str(pre_commit_hook), 'foo')
        path.__str__.assert_called_with()


if __name__ == '__main__':
    unittest.main()
