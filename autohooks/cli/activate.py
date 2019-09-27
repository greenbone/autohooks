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

import sys

from argparse import Namespace

from autohooks.config import (
    load_config_from_pyproject_toml,
    get_pyproject_toml_path,
    AUTOHOOKS_SECTION,
)
from autohooks.install import (
    install_pre_commit_hook,
    get_pre_commit_hook_path,
    get_autohooks_pre_commit_hook,
)
from autohooks.settings import Mode


def install_hooks(args: Namespace) -> None:
    pre_commit_hook_path = get_pre_commit_hook_path()
    pyproject_toml = get_pyproject_toml_path()
    config = load_config_from_pyproject_toml(pyproject_toml)

    if pre_commit_hook_path.exists() and not args.force:
        print(
            'pre-commit hook is already installed at {}. --force to '
            'override.'.format(str(pre_commit_hook_path))
        )
    else:
        if not config.is_autohooks_enabled():
            print(
                'Warning: autohooks is not enabled in your {} file. Please add '
                'a "{}" section. Run autohooks check for more details.'.format(
                    str(pyproject_toml), AUTOHOOKS_SECTION
                ),
                file=sys.stderr,
            )

        if args.mode:
            mode = Mode.from_string(args.mode)
        else:
            mode = config.get_mode()

        autohooks_pre_commit_hook = get_autohooks_pre_commit_hook(mode)
        install_pre_commit_hook(autohooks_pre_commit_hook, pre_commit_hook_path)

        print(
            'pre-commit hook installed at {} using {} mode'.format(
                str(pre_commit_hook_path), str(mode.get_effective_mode())
            )
        )
