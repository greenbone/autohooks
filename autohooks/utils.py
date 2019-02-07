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
import subprocess


def get_git_directory():
    path = os.environ['PWD']
    try:
        output = subprocess.check_output(
            ['git', '-C', path, 'rev-parse', '--git-dir'],
        )
    except subprocess.CalledProcessError as e:
        print('could not determine .git directory. {}'.format(
            e.output.decode()
        ))
        raise e

    gitdir = output.decode().strip()
    if not path in gitdir:
        gitdir = os.path.join(path, gitdir)

    return os.path.abspath(gitdir)


def get_git_hook_directory():
    gitdir = get_git_directory()
    return os.path.join(gitdir, 'hooks')


def get_setup_directory():
    path = os.path.join(os.path.dirname(__file__), os.path.pardir)
    return os.path.abspath(path)
