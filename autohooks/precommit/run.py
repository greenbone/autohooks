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

import importlib
import sys

from autohooks.config import load_config_from_pyproject_toml


def run():
    print('autohooks => pre-commit')

    config = load_config_from_pyproject_toml()
    for name in config.get_pre_commit_script_names():
        try:
            script = importlib.import_module(name)
            retval = script.precommit()

            if retval:
                return retval

        except ImportError as e:
            print(
                'An error occurred while importing pre-commit '
                'hook {}. {}. The hook will be ignored.'.format(name, e),
                file=sys.stderr,
            )
        except Exception as e:
            print(
                'An error occurred while running pre-commit '
                'hook {}. {}. The hook will be ignored.'.format(name, e),
                file=sys.stderr,
            )
    return 0
