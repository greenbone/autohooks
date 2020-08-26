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
import subprocess

from enum import Enum
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import TracebackType
from typing import Any, List, Type, Optional, Generator, Union, TYPE_CHECKING

from autohooks.utils import exec_git, get_project_root_path, GitError

# https://stackoverflow.com/questions/49959656/typing-exit-in-3-5-fails-on-runtime-but-typechecks
if TYPE_CHECKING:
    BaseExceptionType = Type[BaseException]
else:
    BaseExceptionType = bool  # don't care, as long is it doesn't error

__all__ = [
    'exec_git',
    'get_staged_status',
    'get_status',
    'is_partially_staged_status',
    'is_staged_status',
    'stage_files_from_status_list',
    'stash_unstaged_changes',
]


def _get_git_toplevel_path():
    try:
        git_dir = exec_git('rev-parse', '--show-toplevel').rstrip()
    except subprocess.CalledProcessError as e:
        print(
            'could not determine toplevel directory. {}'.format(
                e.output.decode()
            )
        )
        raise e from None
    return Path(git_dir).resolve()


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
    def __init__(self, status_string: str, root_path: Path = None) -> None:
        status = status_string[:2]
        filename = status_string[3:]

        self.index = Status(status[0])
        self.working_tree = Status(status[1])
        self.root_path = root_path

        if self.index == Status.RENAMED:
            new_filename, old_filename = filename.split('\0')
            self.path = Path(new_filename)
            self.old_path = Path(old_filename)
        else:
            self.path = Path(filename)

    def __str__(self) -> str:
        return '{}{} {}'.format(
            self.index.value, self.working_tree.value, str(self.path)
        )

    def __repr__(self) -> str:
        return '<StatusEntry {}>'.format(str(self))

    def absolute_path(self) -> Path:
        if self.root_path:
            return (self.root_path / self.path).resolve()
        return self.path.resolve()


def _parse_status(output: str) -> Generator[str, None, None]:
    output = output.rstrip('\0')
    if not output:
        return

    output_list = output.split('\0')
    while output_list:
        line = output_list.pop(0)
        if line[0] == Status.RENAMED.value:
            yield '{}\0{}'.format(line, output_list.pop(0))
        else:
            yield line


def is_staged_status(status: StatusEntry) -> bool:
    return (
        status.index != Status.UNMODIFIED
        and status.index != Status.UNTRACKED
        and status.index != Status.IGNORED
        and status.index != Status.DELETED
    )


def is_partially_staged_status(status: StatusEntry) -> bool:
    return (
        status.index != Status.UNMODIFIED
        and status.index != Status.UNTRACKED
        and status.index != Status.IGNORED
        and status.index != Status.DELETED
        and status.working_tree != Status.UNMODIFIED
        and status.working_tree != Status.UNTRACKED
        and status.working_tree != Status.IGNORED
    )


def get_status(files: List[Union[Path, str]] = None) -> List[StatusEntry]:
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
    root_path = _get_git_toplevel_path()
    return [StatusEntry(f, root_path) for f in _parse_status(output)]


def get_staged_status(
    files: List[Union[Path, str]] = None
) -> List[StatusEntry]:
    status = get_status(files)
    return [s for s in status if is_staged_status(s)]


def stage_files_from_status_list(status_list: List[StatusEntry]) -> None:
    filenames = [str(s.path) for s in status_list]
    exec_git('add', *filenames)


def get_diff(files: List[StatusEntry] = None) -> str:
    args = ['--no-pager', 'diff']

    if files is not None:
        args.append('--')
        args.extend([str(f.absolute_path()) for f in files])

    return exec_git(*args)


def _write_tree() -> str:
    return exec_git('write-tree').strip()


def _read_tree(ref_or_hashid: str) -> None:
    exec_git('read-tree', ref_or_hashid)


def _checkout_from_index(status_list: List[StatusEntry]) -> None:
    filenames = [str(s.path) for s in status_list]
    exec_git('checkout-index', '-f', '--', *filenames)


def _set_ref(name: str, hashid: str) -> None:
    exec_git('update-ref', name, hashid)


def _get_tree_diff(tree1: str, tree2: str) -> bytes:
    return subprocess.check_output(
        [
            'git',
            'diff-tree',
            '--ignore-submodules',
            '--binary',
            '--no-color',
            '--no-ext-diff',
            '--unified=0',
            tree1,
            tree2,
        ]
    )


def _apply_diff(patch: bytes) -> None:
    with NamedTemporaryFile(mode='wb', buffering=0) as f:
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


INDEX_REF = 'refs/autohooks/index'
WORKING_REF = 'refs/autohooks/working'


class stash_unstaged_changes:  # pylint: disable=invalid-name
    def __init__(self, status_list: List[StatusEntry]) -> None:
        self.partially_staged = [
            s for s in status_list if is_partially_staged_status(s)
        ]

    def stash_changes(self) -> None:
        # save current staging area aka. index
        self.index = _write_tree()
        # add ref to be able to restore index manually
        _set_ref(INDEX_REF, self.index)
        # add changes from files to index
        stage_files_from_status_list(self.partially_staged)
        # save index as working tree
        self.working_tree = _write_tree()
        # add ref to be able to restore working tee manually
        _set_ref(WORKING_REF, self.working_tree)

        # restore index without working tree changes
        # working tree changes are "stashed" now
        _read_tree(self.index)
        _checkout_from_index(self.partially_staged)

    def restore_working_tree(self) -> None:
        # restore working tree
        _read_tree(self.working_tree)
        # checkout working tree
        _checkout_from_index(self.partially_staged)

    def __enter__(self) -> None:
        if self.partially_staged:
            self.stash_changes()

    def __exit__(
        self,
        exc_type: Optional[BaseExceptionType],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Any:
        if not self.partially_staged:
            return

        if exc_type is not None:
            # an error has occurred
            # restore working tree and index as it was before formatting
            self.restore_working_tree()
            _read_tree(self.index)
        else:
            # save formatting changes
            formatted_tree = _write_tree()

            self.restore_working_tree()

            # restore index
            # formatted_tree will be the same as index if no changes are applied
            _read_tree(formatted_tree)

            if formatted_tree != self.index:
                # create diff between index and formatted_tree
                patch = _get_tree_diff(self.index, formatted_tree)
                try:
                    # apply diff to working tree
                    _apply_diff(patch)
                except GitError as e:
                    print(
                        'Found conflicts between plugin and local changes. '
                        'Plugin changes will be ignored for conflicted hunks.',
                        e,
                    )

                    rootpath = get_project_root_path()
                    for path in rootpath.glob('*.rej'):
                        path.unlink()
