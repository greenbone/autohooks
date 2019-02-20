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

from autohooks.api import out
from autohooks.api.path import is_python_path
from autohooks.api.git import get_staged_status, stash_unstaged_changes


def check_pylint_installed():
    try:
        import pylint
    except ImportError:
        raise Exception(
            'Could not find pylint. Please add pylint to your python '
            'environment'
        )


def precommit():
    out('Running pylint pre-commit hook')

    check_pylint_installed()

    files = [f for f in get_staged_status() if is_python_path(f.path)]

    with stash_unstaged_changes(files):
        args = ['pylint']
        args.extend([str(f.absolute_path()) for f in files])

        return subprocess.call(args)
