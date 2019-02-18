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

from enum import Enum
from pathlib import Path

from autohooks.utils import exec_git

__all__ = [
    'exec_git',
    'get_staged_files',
    'get_diff',
    'get_status',
    'stage_file',
]


def get_staged_files(diff_filter='ACM'):
    files = exec_git(
        '--no-pager',  # no pagination
        'diff',
        '--staged',
        '--name-only',
        '--diff-filter={}'.format(diff_filter),
        '--no-ext-diff',
        '-z',  # \0 delimiter
    )
    return files.split('\0')


def get_diff(file=None):
    args = ['--no-pager', 'diff', '--no-ext-diff', '--no-color']

    if file is not None:
        args.extend(['--', str(file)])

    return exec_git(*args)


class Status(Enum):
    UNMODIFIED = ' '
    MODIFIED = 'M'
    ADDED = 'A'
    DELETED = 'D'
    RENAMED = 'R'
    COPIED = 'C'
    UPDATED = 'U'
    UNTRACKED = '?'
    IGNORED = '!'


class StatusEntry:
    def __init__(self, statusString):
        status = statusString[0:2]
        filename = statusString[3:]

        self.path = Path(filename)
        self.index = Status(status[0])
        self.workTree = Status(status[1])

    def __str__(self):
        return '{}{} {}'.format(
            self.index.value, self.workTree.value, str(self.path)
        )

    def __repr__(self):
        return '<StatusEntry {}>'.format(str(self))


def get_status(file=None):
    args = ['status', '--porcelain=v1', '-z']

    if file is not None:
        args.extend(['--', str(file)])

    output = exec_git(*args)
    output = output.split('\0')
    return [StatusEntry(f) for f in output if f]


def stage_file(filename):
    exec_git('add', filename)
