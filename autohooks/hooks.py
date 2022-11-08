# Copyright (C) 2019-2022 Greenbone Networks GmbH
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

import re
from pathlib import Path

from autohooks.settings import Mode
from autohooks.template import (
    PIPENV_MULTILINE_SHEBANG,
    PIPENV_SHEBANG,
    POETRY_MULTILINE_SHEBANG,
    POETRY_SHEBANG,
    PYTHON3_SHEBANG,
    TEMPLATE_VERSION,
    PreCommitTemplate,
)
from autohooks.utils import get_git_hook_directory_path


def get_pre_commit_hook_path():
    git_hook_dir_path = get_git_hook_directory_path()
    return git_hook_dir_path / "pre-commit"


class PreCommitHook:
    def __init__(self, pre_commit_hook_path: Path = None) -> None:
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
        lines = self.pre_commit_hook.split("\n")
        # seems to be false-positive ...
        return len(lines) > 5 and "autohooks.precommit" in self.pre_commit_hook

    def is_current_autohooks_pre_commit_hook(self) -> bool:
        return self.read_version() == TEMPLATE_VERSION

    def read_mode(self) -> Mode:
        lines = self.pre_commit_hook.split("\n")
        if len(lines) < 1 or len(lines[0]) == 0:
            return Mode.UNDEFINED

        shebang = lines[0][2:]

        if shebang == PYTHON3_SHEBANG:
            return Mode.PYTHONPATH
        if shebang.startswith(POETRY_SHEBANG):
            return Mode.POETRY
        if shebang == PIPENV_SHEBANG:
            return Mode.PIPENV

        shebang = f"{lines[0][2:]}\n"
        shebang += "\n".join(lines[1:5])
        if shebang == POETRY_MULTILINE_SHEBANG:
            return Mode.POETRY_MULTILINE

        if shebang == PIPENV_MULTILINE_SHEBANG:
            return Mode.PIPENV_MULTILINE

        return Mode.UNKNOWN

    def read_version(self) -> int:
        matches = re.search(
            r"{\s*version\s*=\s*?(\d+)\s*}$", self.pre_commit_hook, re.MULTILINE
        )
        if not matches:
            return -1

        return int(matches.group(1))

    def write(self, *, mode: Mode) -> None:
        template = PreCommitTemplate()
        pre_commit_hook = template.render(mode=mode)

        self.pre_commit_hook_path.write_text(pre_commit_hook)
        self.pre_commit_hook_path.chmod(0o775)

        self._pre_commit_hook = None

    def __str__(self) -> str:
        return str(self.pre_commit_hook_path)
