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

from autohooks.utils import exec_git

__all__ = ['exec_git', 'get_staged_files', 'get_diff', 'stage_file']


def get_staged_files(diff_filter='ACM'):
    files = exec_git(
        '-P',  # no pagination
        'diff',
        '--staged',
        '--name-only',
        '--diff-filter={}'.format(diff_filter),
        '--no-ext-diff',
        '-z',  # \0 delimiter
    )
    return files.split('\0')


def get_diff(file=None):
    args = ['-P', 'diff', '--no-ext-diff', '--no-color']

    if file is not None:
        args.extend(['--', str(file)])

    return exec_git(*args)


def stage_file(filename):
    exec_git('add', filename)
