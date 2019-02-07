# Copyright (C) 2017-2019 Greenbone Networks GmbH
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

from setuptools.command.install import install

from .utils import get_git_hook_directory, get_setup_directory


class PostInstall(install):

    def run(self):
        install.run(self)
        self.post_install()

    def post_install(self):
        githookdir = get_git_hook_directory()
        pre_commit_hook = os.path.join(githookdir, 'pre-commit')
        if os.path.exists(pre_commit_hook):
            print('pre-commit hook already installed')
        else:
            setup_path = get_setup_directory()
            pre_commit_file = os.path.join(setup_path, 'pre-commit')
            shutil.copy(pre_commit_file, pre_commit_hook)
            print('pre-commit hook installed at {}'.format(pre_commit_hook))
