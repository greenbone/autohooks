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

import os
import subprocess

from pathlib import Path


def exec_git(*args, ignore_errors=False):
    try:
        cmd_args = ['git']
        cmd_args.extend(args)
        output = subprocess.check_output(cmd_args)
        return output.decode()
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            return ''
        raise e


def get_git_directory_path():
    pwd = os.environ['PWD']
    try:
        git_dir = exec_git('-C', pwd, 'rev-parse', '--git-dir').rstrip()
    except subprocess.CalledProcessError as e:
        print(
            'could not determine .git directory. {}'.format(e.output.decode())
        )
        raise e

    if pwd and not pwd in git_dir:
        git_dir_path = Path(pwd) / git_dir
    else:
        git_dir_path = Path(git_dir)

    return git_dir_path.resolve()


def get_autohooks_directory_path():
    return Path(__file__).resolve().parent


def get_git_hook_directory_path():
    git_dir_path = get_git_directory_path()
    return git_dir_path / 'hooks'


def is_project_root(path):
    return (
        (path / 'pyproject.toml').is_file()
        or (path / '.git').is_dir()
        or (path / 'setup.py').is_file()
        or (path / 'setup.cfg').is_file()
    )


def get_project_root_path():
    path = Path(os.environ['PWD'])
    path.resolve()

    if is_project_root(path):
        return path

    for parent in path.parents:
        if is_project_root(parent):
            return parent

    return path


def get_pyproject_toml_path():
    root = get_project_root_path()
    return root / 'pyproject.toml'
