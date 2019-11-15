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
from autohooks.hooks import PreCommitHook


class AutohooksInstall:
    def install_git_hook(self) -> None:
        try:
            pre_commit_hook = PreCommitHook()
            if not pre_commit_hook.exists():
                config = load_config_from_pyproject_toml()
                pre_commit_hook.write(mode=config.get_mode())
        except Exception:  # pylint: disable=broad-except
            pass


class PostInstall(install, AutohooksInstall):
    def run(self) -> None:
        super().run()
        self.install_git_hook()


class PostDevelop(develop, AutohooksInstall):
    def install_for_development(self) -> None:
        super().install_for_development()
        self.install_git_hook()
