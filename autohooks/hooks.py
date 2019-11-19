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

from pathlib import Path

import toml

from autohooks.settings import Mode
from autohooks.template import (
    PIPENV_SHEBANG,
    POETRY_SHEBANG,
    PYTHON3_SHEBANG,
    TEMPLATE_VERSION,
    PreCommitTemplate,
)
from autohooks.utils import get_git_hook_directory_path


def get_pre_commit_hook_path():
    git_hook_dir_path = get_git_hook_directory_path()
    return git_hook_dir_path / 'pre-commit'


class PreCommitHook:
    def __init__(self, pre_commit_hook_path: Path = None):
        self._pre_commit_hook = None

        if pre_commit_hook_path is None:
            self.pre_commit_hook_path = get_pre_commit_hook_path()
        else:
            self.pre_commit_hook_path = pre_commit_hook_path

    @property
    def pre_commit_hook(self) -> str:
        if self._pre_commit_hook is None:
            self._pre_commit_hook = self.pre_commit_hook_path.read_text()

        return self._pre_commit_hook

    def exists(self) -> bool:
        return self.pre_commit_hook_path.exists()

    def is_autohooks_pre_commit_hook(self) -> bool:
        lines = self.pre_commit_hook.split('\n')
        return len(lines) > 5 and "autohooks.precommit" in self.pre_commit_hook

    def is_current_autohooks_pre_commit_hook(self) -> bool:
        return self.read_version() == TEMPLATE_VERSION

    def read_mode(self) -> Mode:
        lines = self.pre_commit_hook.split('\n')
        if len(lines) < 1 or len(lines[0]) == 0:
            return Mode.UNDEFINED

        shebang = lines[0][2:]

        if shebang == PYTHON3_SHEBANG:
            return Mode.PYTHONPATH
        if shebang == POETRY_SHEBANG:
            return Mode.POETRY
        if shebang == PIPENV_SHEBANG:
            return Mode.PIPENV

        return Mode.UNKNOWN

    def read_version(self) -> int:
        lines = self.pre_commit_hook.split('\n')
        if len(lines) < 2:
            return -1

        try:
            parsed = toml.loads(lines[1][1:])
        except toml.TomlDecodeError:
            return -1

        try:
            meta = parsed['meta']
            return int(meta['version'])
        except KeyError:
            return -1

    def write(self, *, mode: Mode):
        template = PreCommitTemplate()
        pre_commit_hook = template.render(mode=mode)

        self.pre_commit_hook_path.write_text(pre_commit_hook)
        self.pre_commit_hook_path.chmod(0o775)

        self._pre_commit_hook = None

    def __str__(self) -> str:
        return str(self.pre_commit_hook_path)
