# Copyright (C) 2019-2022 Greenbone Networks GmbH
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

"""
Plugin API for handling git related tasks
"""

import os
import subprocess
from enum import Enum
from os import PathLike
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import TracebackType
from typing import Any, Iterable, Iterator, List, Optional, Type

from autohooks.utils import GitError, exec_git, get_project_root_path

__all__ = [
    "exec_git",
    "GitError",
    "get_staged_status",
    "get_status",
    "is_partially_staged_status",
    "is_staged_status",
    "stage_files",
    "stash_unstaged_changes",
    "StatusEntry",
    "Status",
]


def _get_git_toplevel_path():
    try:
        git_dir = exec_git("rev-parse", "--show-toplevel").rstrip()
    except subprocess.CalledProcessError as e:
        print("could not determine toplevel directory. {e.output.decode()}")
        raise e from None
    return Path(git_dir).resolve()


class Status(Enum):
    """
    Status of a file in git
    """

    UNMODIFIED = " "
    MODIFIED = "M"
    ADDED = "A"
    DELETED = "D"
    RENAMED = "R"
    COPIED = "C"
    UPDATED = "U"
    UNTRACKED = "?"
    IGNORED = "!"


class StatusEntry:
    """
    Status of a file in the git index and working tree.

    Implements the :py:class:`os.PathLike` protocol.

    Attributes:
        index: Status in the index
        working_tree: Status in the working tree
        path: Path to the file
        root_path: An optional path to a root directory
        old_path: Set for renamed files
    """

    def __init__(self, status_string: str, root_path: Path = None) -> None:
        status = status_string[:2]
        filename = status_string[3:]

        # Status in the index
        self.index = Status(status[0])
        # Status in the working directory
        self.working_tree = Status(status[1])
        self.root_path = root_path

        if self.index == Status.RENAMED:
            new_filename, old_filename = filename.split("\0")
            self.path = Path(new_filename)
            self.old_path = Path(old_filename)
        else:
            # path of the file in git
            self.path = Path(filename)

    def __str__(self) -> str:
        return f"{self.index.value}{self.working_tree.value} {str(self.path)}"

    def __repr__(self) -> str:
        return f"<StatusEntry {str(self)}>"

    def absolute_path(self) -> Path:
        """
        Returns the absolute path of the file of this StatusEntry
        """
        if self.root_path:
            return (self.root_path / self.path).resolve()
        return self.path.resolve()

    def __fspath__(self):
        return self.path.__fspath__()


def _parse_status(output: str) -> Iterator[str]:
    output = output.rstrip("\0")
    if not output:
        return

    output_list = output.split("\0")
    while output_list:
        line = output_list.pop(0)
        if line[0] == Status.RENAMED.value:
            yield f"{line}\0{output_list.pop(0)}"
        else:
            yield line


def is_staged_status(status: StatusEntry) -> bool:
    """Returns true, if the status of the given :py:class:`StatusEntry` is
    staged.

    Arguments:
        status: A :py:class:`StatusEntry` object that contains the filename,
            path and the git status.

    Returns:
        True if file is staged, False else.
    """
    return (
        status.index != Status.UNMODIFIED
        and status.index != Status.UNTRACKED
        and status.index != Status.IGNORED
        and status.index != Status.DELETED
    )


def is_partially_staged_status(status: StatusEntry) -> bool:
    """Returns true, if the status of the given :py:class:`StatusEntry`
    is partially staged.

    Arguments:
        status: A :py:class:`StatusEntry` object that contains the filename,
            path and the git status.

    Returns:
        True if file is partially staged, False else.
    """
    return (
        status.index != Status.UNMODIFIED
        and status.index != Status.UNTRACKED
        and status.index != Status.IGNORED
        and status.index != Status.DELETED
        and status.working_tree != Status.UNMODIFIED
        and status.working_tree != Status.UNTRACKED
        and status.working_tree != Status.IGNORED
    )


def get_status(files: Optional[Iterable[PathLike]] = None) -> List[StatusEntry]:
    """Get information about the current git status.

    Arguments:
        files: (optional) specify an iterable of :py:class:`os.PathLike` and
            exclude all other paths for the status.

    Returns:
        A list of :py:class:`StatusEntry` instances that contain the status of
        the specific files.
    """
    args = [
        "status",
        "-z",
        "--ignore-submodules",
        "--untracked-files=no",
    ]

    if files is not None:
        args.append("--")
        args.extend([os.fspath(f) for f in files])

    output = exec_git(*args)
    root_path = _get_git_toplevel_path()
    return [StatusEntry(f, root_path) for f in _parse_status(output)]


def get_staged_status(
    files: Optional[Iterable[PathLike]] = None,
) -> List[StatusEntry]:
    """Get a list of :py:class:`StatusEntry` instances containing only staged
    files.

    Arguments:
        files: (optional) specify an iterable of files and exclude all other
            paths for the status.

    Returns:
        A list of :py:class:`StatusEntry` instances with files that are staged.
    """
    status = get_status(files)
    return [s for s in status if is_staged_status(s)]


def stage_files_from_status_list(status_list: Iterable[StatusEntry]) -> None:
    """Add the passed files from the status list to git staging index

    Deprecated. Please use stage_files instead.

    Arguments:
        status_list: A List of StatusEntry instances that should be added
    """
    stage_files(status_list)


def stage_files(files: Iterable[PathLike]) -> None:
    """Add the passed :py:class:`os.PathLike` to git staging index

    Arguments:
        files: An iterable of :py:class:`os.PathLike` to add to the index
    """
    filenames = [os.fspath(f) for f in files]
    exec_git("add", *filenames)


def get_diff(files: Optional[Iterable[StatusEntry]] = None) -> str:
    """Get the diff of the passed files

    Arguments:
        status_list: A List of StatusEntry instances that should be diffed

    Returns:
        string containing the diff of the given files
    """
    args = ["--no-pager", "diff"]

    if files is not None:
        args.append("--")
        args.extend([str(f.absolute_path()) for f in files])

    return exec_git(*args)


def _write_tree() -> str:
    """
    Create a tree object from the current index

    Returns:
        The name of the new tree object
    """
    return exec_git("write-tree").strip()


def _read_tree(ref_or_hashid: str) -> None:
    """
    Loads (reads) tree information into the index

    Arguments:
        ref_or_hashid: Git hash or ref to load into the index
    """
    exec_git("read-tree", ref_or_hashid)


def _checkout_from_index(files: Iterable[PathLike]) -> None:
    """
    Copy all files listed from the index to the working directory

    Arguments:
        files: Iterable of files that should be checked out into the working
               directory
    """
    filenames = [os.fspath(s) for s in files]
    exec_git("checkout-index", "-f", "--", *filenames)


def _set_ref(name: str, hashid: str) -> None:
    """
    Create a git ref for a hash

    Arguments:
        name: Name of the reference to be created
        hashid: Hash that the reference should point to
    """
    exec_git("update-ref", name, hashid)


def _get_tree_diff(tree1: str, tree2: str) -> bytes:
    """
    Calculate a diff between two tree objects

    Returns:
        The diff as bytes
    """
    return subprocess.check_output(
        [
            "git",
            "diff-tree",
            "--ignore-submodules",
            "--binary",
            "--no-color",
            "--no-ext-diff",
            "--unified=0",
            tree1,
            tree2,
        ]
    )


def _apply_diff(patch: bytes) -> None:
    with NamedTemporaryFile(mode="wb", buffering=0) as f:
        f.write(patch)

        exec_git(
            "apply",
            "-v",
            "--whitespace=nowarn",
            "--reject",
            "--recount",
            "--unidiff-zero",
            f.name,
        )


INDEX_REF = "refs/autohooks/index"
WORKING_REF = "refs/autohooks/working"


class stash_unstaged_changes:  # pylint: disable=invalid-name
    """
    A context manager that stashes changes on tracked files that are not added
    to the index. The stashed changes are restored when the context manager
    exits.

    Example: ::

        with stash_unstaged_changes():
            do_something()
    """

    def __init__(self, files: Optional[Iterable[PathLike]] = None) -> None:
        """
        Args:
            files: Optional iterable of path like objects to consider for being
                staged. By default all files in the git status are considered.
        """
        status_list = get_status(files)
        self.partially_staged = [
            s for s in status_list if is_partially_staged_status(s)
        ]

    def _stash_changes(self) -> None:
        # save current staging area aka. index
        self.index = _write_tree()
        # add ref to be able to restore index manually
        _set_ref(INDEX_REF, self.index)
        # add changes from files to index
        stage_files(self.partially_staged)
        # save index as working tree
        # unstaged changes are stored in the working tree now
        self.working_tree = _write_tree()
        # add ref to be able to restore working tree manually
        _set_ref(WORKING_REF, self.working_tree)

        # restore index without working tree changes
        # working tree changes are "stashed" now
        _read_tree(self.index)
        _checkout_from_index(self.partially_staged)

    def _restore_working_tree(self) -> None:
        # restore working tree
        _read_tree(self.working_tree)
        # checkout working tree
        _checkout_from_index(self.partially_staged)

    def __enter__(self) -> None:
        if self.partially_staged:
            self._stash_changes()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Any:
        if not self.partially_staged:
            return

        if exc_type is not None:
            # an error has occurred
            # restore working tree and index as it was before formatting
            self._restore_working_tree()
            _read_tree(self.index)
        else:
            # save possible changes made to the index
            changed_tree = _write_tree()

            self._restore_working_tree()

            # restore index
            _read_tree(changed_tree)

            # create and apply diff between index before running the plugin and
            # changes made by the plugin if some changes have been applied and
            # staged.
            # changed_tree will be the same as index if no changes are applied.
            # changed_tree may be the same as the working tree. in that case no
            # further action is needed.
            if changed_tree != self.index and changed_tree != self.working_tree:
                # create diff between working tree and changed tree
                patch = _get_tree_diff(self.index, changed_tree)
                try:
                    # apply diff to working tree
                    _apply_diff(patch)
                except GitError as e:
                    print(
                        "Found conflicts between plugin and local changes. "
                        "Plugin changes will be ignored for conflicted hunks.",
                        e,
                    )

                    rootpath = get_project_root_path()
                    for path in rootpath.glob("*.rej"):
                        path.unlink()
