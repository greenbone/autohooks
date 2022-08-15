# -*- coding: utf-8 -*-
# Copyright (C) 2022 Greenbone Networks GmbH
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
import sys
import tempfile
from contextlib import AbstractContextManager, contextmanager
from pathlib import Path
from typing import Generator, Optional

from autohooks.utils import exec_git


class AddSysPath(AbstractContextManager):
    """
    Context Manager to add a directory path to the module search path aka.
    sys.path. The directory path

    Example:
        with AddSysPath("")
    """

    def __init__(self, directory: Path):
        self.directory = str(directory.resolve())

        if sys.path[0] != self.directory:
            sys.path.insert(0, self.directory)

    def cleanup(self):
        try:
            sys.path.remove(self.directory)
        except ValueError:
            # self.directory was not in the path
            pass

    def __exit__(self, __exc_type, __exc_value, __traceback) -> None:
        self.cleanup()


@contextmanager
def tempdir(
    change_into: bool = False, add_to_sys_path: bool = False
) -> Generator[Path, None, None]:
    """
    Context Manager to create a temporary directory

    Args:
        change_into: Set the created temporary as the current working directory
        add_to_sys_path: Add the created temporary directory to the directories
            for searching for Python modules

    Returns:
        A path to the created temporary directory
    """
    temp_dir = tempfile.TemporaryDirectory()
    dir_path = Path(temp_dir.name)

    if change_into:
        os.chdir(dir_path)

    if add_to_sys_path:
        sys_path = AddSysPath(dir_path)

    yield Path(dir_path)

    if add_to_sys_path:
        sys_path.cleanup()

    temp_dir.cleanup()


@contextmanager
def tempgitdir() -> Generator[Path, None, None]:
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name)

    os.chdir(str(temp_path))

    exec_git("init", "-b", "main")
    exec_git("config", "--local", "user.email", "max.mustermann@example.com")
    exec_git("config", "--local", "user.name", "Max Mustermann")

    yield temp_path

    temp_dir.cleanup()


@contextmanager
def temp_file(
    content: str,
    *,
    name: Optional[str] = "test.toml",
    change_into: bool = False,
) -> Generator[Path, None, None]:
    """
    A Context Manager to create a temporary file within a new temporary
    directory. The temporary file and directory are removed when the context is
    exited.

    Args:
        content: Content to write into the temporary file.
        name: Name of the temporary file. "test.toml" by default.
        change_into: Adjust the current working directory to the temporary
            directory.
    """
    with tempdir(change_into=change_into) as tmp_dir:
        test_file = tmp_dir / name
        test_file.write_text(content, encoding="utf8")
        yield test_file


@contextmanager
def temp_python_module(
    content: str, *, name="foo"
) -> Generator[Path, None, None]:
    """
    A Context Manager to create a new Python module in a temporary directory.
    The temporary directory will be added to the module search path and removed
    from the search path when the context is exited. Also it is ensured that
    the module is unloaded if the context is exited.

    Args:
        content: Python code to write into the temporary module.
        name: Name of the new Python module. By default: "foo".

    Example:
        with temp_python_module("print()", name="bar") as python_module_path
    """
    with tempdir(
        add_to_sys_path=True,
    ) as tmp_dir, ensure_unload_module(name):
        test_file = tmp_dir / f"{name}.py"
        test_file.write_text(content, encoding="utf8")
        yield test_file


def unload_module(name: str) -> None:
    """
    Unload a Python module
    """
    if name in sys.modules:
        del sys.modules[name]


@contextmanager
def ensure_unload_module(name: str) -> Generator[None, None, None]:
    """
    Ensure that a module gets removed even if an error occurs

    Example:
        with ensure_unload_module("foo.bar"):
            do_something()
    """
    yield
    unload_module(name)
