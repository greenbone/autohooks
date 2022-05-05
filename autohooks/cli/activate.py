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

from argparse import Namespace

from autohooks.config import (
    get_pyproject_toml_path,
    load_config_from_pyproject_toml,
)
from autohooks.hooks import PreCommitHook
from autohooks.settings import Mode
from autohooks.terminal import Terminal


def install_hooks(term: Terminal, args: Namespace) -> None:
    pre_commit_hook = PreCommitHook()
    pyproject_toml = get_pyproject_toml_path()
    config = load_config_from_pyproject_toml(pyproject_toml)

    if pre_commit_hook.exists() and not args.force:
        term.ok(
            "autohooks pre-commit hook is already"
            f" installed at {str(pre_commit_hook)}."
        )
        with term.indent():
            term.print()
            term.info(
                "Run 'autohooks activate --force' to override the current "
                "installed pre-commit hook."
            )
            term.info(
                "Run 'autohooks check' to validate the current status of "
                "the installed pre-commit hook."
            )
    else:
        if not config.is_autohooks_enabled():
            term.warning(
                f"autohooks is not enabled in your {str(pyproject_toml)} "
                "file. Run 'autohooks check' for more details."
            )

        if args.mode:
            mode = Mode.from_string(args.mode)
        else:
            mode = config.get_mode()

        pre_commit_hook.write(mode=mode)

        term.ok(
            f"autohooks pre-commit hook installed at {str(pre_commit_hook)}"
            f" using {str(mode.get_effective_mode())} mode."
        )
