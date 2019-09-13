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

from setuptools.command.install import install
from setuptools.command.develop import develop

from autohooks.config import load_config_from_pyproject_toml
from autohooks.template import PreCommitTemplate

from autohooks.utils import get_git_hook_directory_path


def get_pre_commit_hook_path():
    git_hook_dir_path = get_git_hook_directory_path()
    return git_hook_dir_path / 'pre-commit'


def get_autohooks_pre_commit_hook(mode):
    template = PreCommitTemplate()

    return template.render(mode=mode)


def is_autohooks_pre_commit_hook(path):
    hook = path.read_text()
    lines = hook.split('\n')
    return len(lines) > 5 and "autohooks.precommit" in lines[5]


def install_pre_commit_hook(pre_commit_hook, pre_commit_hook_path):
    pre_commit_hook_path.write_text(pre_commit_hook)
    pre_commit_hook_path.chmod(0o775)


class AutohooksInstall:
    def install_git_hook(self):
        try:
            pre_commit_hook_path = get_pre_commit_hook_path()
            if not pre_commit_hook_path.exists():
                config = load_config_from_pyproject_toml()

                mode = config.get_mode()
                autohooks_pre_commit_hook = get_autohooks_pre_commit_hook(mode)
                install_pre_commit_hook(
                    autohooks_pre_commit_hook, pre_commit_hook_path
                )
        except Exception:  # pylint: disable=broad-except
            pass


class PostInstall(install, AutohooksInstall):
    def run(self):
        super().run()
        self.install_git_hook()


class PostDevelop(develop, AutohooksInstall):
    def install_for_development(self):
        super().install_for_development()
        self.install_git_hook()
