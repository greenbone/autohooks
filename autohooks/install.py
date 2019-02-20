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
import shutil
import subprocess

from setuptools.command.install import install
from setuptools.command.develop import develop

from .config import load_config_from_pyproject_toml
from .utils import get_git_hook_directory_path, get_autohooks_directory_path


def get_pre_commit_hook_path():
    git_hook_dir_path = get_git_hook_directory_path()
    return git_hook_dir_path / 'pre-commit'


def get_pre_commit_hook_template_path():
    setup_dir_path = get_autohooks_directory_path()
    return setup_dir_path / 'precommit' / 'template'


def install_pre_commit_hook(pre_commit_hook_file, pre_commit_hook):
    shutil.copy(str(pre_commit_hook_file), str(pre_commit_hook))


class AutohooksInstall:
    def install_git_hook(self):
        try:
            pre_commit_hook = get_pre_commit_hook_path()
            if not pre_commit_hook.exists():
                pre_commit_hook_template = get_pre_commit_hook_template_path()
                install_pre_commit_hook(
                    pre_commit_hook_template, pre_commit_hook
                )
        except subprocess.CalledProcessError:
            pass


class PostInstall(install, AutohooksInstall):
    def run(self):
        super().run()
        self.install_git_hook()


class PostDevelop(develop, AutohooksInstall):
    def install_for_development(self):
        super().install_for_development()
        self.install_git_hook()
