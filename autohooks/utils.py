# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import shlex
import subprocess
from pathlib import Path
from typing import List, Optional


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
        cmd_args: List[str] = ["git"]
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
    """
    Returns the path to the git dir.

    Returns:
        Absolute path to .git dir.
    """
    pwd = Path.cwd()

    git_dir = exec_git("-C", str(pwd), "rev-parse", "--git-dir").rstrip()

    if pwd and str(pwd) not in git_dir:
        git_dir_path = Path(pwd) / git_dir
    else:
        git_dir_path = Path(git_dir)

    return git_dir_path.resolve()


def get_autohooks_directory_path() -> Path:
    """
    Returns the path to package dir.

    Returns:
        Absolute path to package dir.
    """

    return Path(__file__).resolve().parent


def get_git_hook_directory_path(git_dir_path: Optional[Path] = None) -> Path:
    """
    Returns the absolute path to git hooks dir.

    Args:
        git_dir_path: Path to .git dir.

    Returns:
        Absolute path to git hooks dir.
    """

    if git_dir_path is None:
        git_dir_path = get_git_directory_path()
    return git_dir_path / "hooks"


def is_project_root(path: Path) -> bool:
    """
    Checks if the given dir is the project root dir.
    The dir is considered a project root if it contains any of:
    - pyproject.toml
    - .git dir
    - setup.py
    - setup.cfg

    Args:
        path: Path object to check for project root

    Returns:
        True if path is project root, False else
    """

    return (
        (path / "pyproject.toml").is_file()
        or (path / ".git").is_dir()
        or (path / "setup.py").is_file()
        or (path / "setup.cfg").is_file()
    )


def get_project_root_path(path: Optional[Path] = None) -> Path:
    """
    Returns the path to the project root dir.

    Args:
        path: Path to the current working dir.

    Returns:
        Absolute path to the project root dir.
    """

    if path is None:
        path = Path.cwd()

    path.resolve()

    if is_project_root(path):
        return path

    for parent in path.parents:
        if is_project_root(parent):
            return parent

    return path


def get_project_autohooks_plugins_path(path: Optional[Path] = None) -> Path:
    """
    Returns the path to plugins folder.

    Args:
        path: Path to the current working dir.

    Returns:
        Absolute path to plugins dir.
    """

    root = get_project_root_path(path)
    return root / ".autohooks"


def get_pyproject_toml_path(path: Optional[Path] = None) -> Path:
    """
    Returns the path to pyproject.toml.

    Args:
        path: Path to the current working dir.

    Returns:
        Absolute path to pyproject.toml.
    """

    root = get_project_root_path(path)
    return root / "pyproject.toml"


def is_split_env():
    """
    Checks that environment supports -S option (separate arguments).

    Returns:
        True: if OS is modern Linux/BSD
        False: if OS is older/macOS/Windows
    """

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
