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
from tempfile import NamedTemporaryFile

from autohooks.utils import exec_git

__all__ = [
    'exec_git',
    'get_staged_files',
    'get_diff',
    'get_status',
    'stage_file',
]


def get_staged_files(diff_filter=None):
    if diff_filter is None:
        diff_filter = [Status.ADDED, Status.COPIED, Status.MODIFIED]

    files = exec_git(
        '--no-pager',  # no pagination
        'diff',
        '--staged',
        '--name-only',
        '--diff-filter={}'.format(''.join([s.value for s in diff_filter])),
        '--no-ext-diff',
        '--no-color',
        '-z',  # \0 delimiter
    )
    return files.rstrip('\0').split('\0')


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
    def __init__(self, status_string):
        status = status_string[:2]
        filename = status_string[3:]

        self.index = Status(status[0])
        self.work_tree = Status(status[1])

        if self.index == Status.RENAMED:
            new_filename, old_filename = filename.split('\0')
            self.path = Path(new_filename)
            self.old_path = Path(old_filename)
        else:
            self.path = Path(filename)

    def __str__(self):
        return '{}{} {}'.format(
            self.index.value, self.work_tree.value, str(self.path)
        )

    def __repr__(self):
        return '<StatusEntry {}>'.format(str(self))


def parse_status(output):
    output = output.rstrip('\0')
    if not output:
        raise StopIteration()

    output = output.split('\0')
    while output:
        line = output.pop(0)
        if line[0] == Status.RENAMED.value:
            yield '{}\0{}'.format(line, output.pop(0))
        else:
            yield line


def get_status(files=None):
    args = [
        'status',
        '--porcelain=v1',
        '-z',
        '--ignore-submodules',
        '--untracked-files=no',
    ]

    if files is not None:
        args.append('--')
        args.extend([str(f) for f in files])

    output = exec_git(*args)
    return [StatusEntry(f) for f in parse_status(output)]


def stage_file(filename):
    stage_files([filename])


def stage_files(filenames):
    exec_git('add', *filenames)


def write_tree():
    return exec_git('write-tree').strip()


def read_tree(ref_or_hashid):
    exec_git('read-tree', ref_or_hashid)


def checkout_index():
    exec_git('checkout-index', '-a', '-f')


def get_tree_diff(tree1, tree2):
    return exec_git(
        'diff-tree',
        '--ignore-submodules',
        '--binary',
        '--no-color',
        '--no-ext-diff',
        'unified=0',
        tree1,
        tree2,
    )


def apply_diff(patch):
    with NamedTemporaryFile(mode='w') as f:
        f.write(patch)

        exec_git(
            'apply',
            '-v',
            '--whitespace=nowarn',
            '--reject',
            '--recount',
            '--unidiff-zero',
            f.name,
        )


class save_formatting:
    def __init__(self, filenames):
        self.filenames = filenames

    def stash_unstaged_changes(self):
        # save current staging area aka. index
        self.index = write_tree()
        # add changes from files to index
        stage_files(self.filenames)
        # save index as working tree
        self.working_tree = write_tree()

        # restore index without working tree changes
        # working tree changes are "stashed" now
        read_tree(self.index)
        checkout_index()

    def restore_working_tree(self):
        # restore working tree
        read_tree(self.working_tree)
        # checkout working tree
        checkout_index()

    def __enter__(self):
        self.stash_unstaged_changes()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            # an error has occurred
            # restore working tree and index as it was before formatting
            self.restore_working_tree()
            read_tree(self.index)
        else:
            # save formatting changes
            formatted_tree = write_tree()

            self.restore_working_tree()

            if formatted_tree == self.index:
                # no formatting changes
                # restore index
                read_tree(self.index)
            else:
                # read formatted changes into index
                read_tree(formatted_tree)
                # create diff between index and formatted_tree
                patch = get_tree_diff(self.index, formatted_tree)
                # apply diff to working tree
                apply_diff(patch)
