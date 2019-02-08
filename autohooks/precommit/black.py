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

import subprocess

from autohooks.api import (
    get_staged_files,
    is_python_file,
    get_git_diff,
    git_stage_file,
)


def check_black_installed():
    try:
        import black
    except ImportError:
        raise Exception(
            'Could not find black. Please add black to your python environment.'
        )


def run():
    print('Running black pre-commit hook')

    check_black_installed()

    files = [f for f in get_staged_files() if is_python_file(f)]

    print('Running black on {}'.format(','.join(files)))

    for f in files:
        before = get_git_diff()
        subprocess.check_call(['black', '-q', f])
        after = get_git_diff()
        if before != after:
            git_stage_file(f)

    return 0
