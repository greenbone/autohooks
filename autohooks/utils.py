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

import shlex
import subprocess
from pathlib import Path


class GitError(subprocess.CalledProcessError):
    """
    Error raised if a git command fails.
    """

    def __str__(self) -> str:
        return (
            f"Git command '{self.cmd}' returned "
            f"non-zero exit status {str(self.returncode)}"
        )


def exec_git(*args: str, ignore_errors: bool = False) -> str:
    """
    Execute git command.

    Raises:
        GitError: A GitError is raised if the git commit fails and ignore_errors
            is False.

    Args:
        *args: Variable length argument list passed to git.
        ignore_errors: Ignore errors if git command fails. Default: False.

    Example: ::

        exec_git("commit", "-m", "A new commit")
    """
    try:
        cmd_args = ["git"]
        cmd_args.extend(args)
        process = subprocess.run(
            cmd_args, check=True, capture_output=True, text=True
        )
        return process.stdout
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            return ""
        raise GitError(e.returncode, e.cmd, e.output, e.stderr) from None


def get_git_directory_path() -> Path:
    pwd = Path.cwd()

    git_dir = exec_git("-C", pwd, "rev-parse", "--git-dir").rstrip()

    if pwd and str(pwd) not in git_dir:
        git_dir_path = Path(pwd) / git_dir
    else:
        git_dir_path = Path(git_dir)

    return git_dir_path.resolve()


def get_autohooks_directory_path() -> Path:
    return Path(__file__).resolve().parent


def get_git_hook_directory_path(git_dir_path: Path = None) -> Path:
    if git_dir_path is None:
        git_dir_path = get_git_directory_path()
    return git_dir_path / "hooks"


def is_project_root(path: Path) -> bool:
    return (
        (path / "pyproject.toml").is_file()
        or (path / ".git").is_dir()
        or (path / "setup.py").is_file()
        or (path / "setup.cfg").is_file()
    )


def get_project_root_path(path: Path = None) -> Path:
    if path is None:
        path = Path.cwd()

    path.resolve()

    if is_project_root(path):
        return path

    for parent in path.parents:
        if is_project_root(parent):
            return parent

    return path


def get_project_autohooks_plugins_path(path: Path = None) -> Path:
    root = get_project_root_path(path)
    return root / ".autohooks"


def get_pyproject_toml_path(path: Path = None) -> Path:
    root = get_project_root_path(path)
    return root / "pyproject.toml"


def is_split_env():
    try:
        subprocess.run(
            shlex.split("/usr/bin/env -S echo True"),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=True,
        )
        is_split = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        is_split = False

    return is_split
