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
from .utils import exec_git


def is_python_file(filename=''):
    return filename.endswith('.py')


def get_staged_files(diff_filter='ACM'):
    files = exec_git(
        'diff',
        '--staged',
        '--name-only',
        '--diff-filter={}'.format(diff_filter),
        '--no-ext-diff',
    )
    return files.split('\n')


def get_git_diff():
    return exec_git('diff', '--no-ext-diff', '--no-color')


def git_stage_file(filename):
    exec_git('add', filename)
