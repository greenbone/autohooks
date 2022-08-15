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

import argparse
import sys

from autohooks.__version__ import __version__ as version
from autohooks.cli.activate import install_hooks
from autohooks.cli.check import check_hooks
from autohooks.cli.plugins import (
    add_plugins,
    list_plugins,
    plugins,
    remove_plugins,
)
from autohooks.settings import Mode
from autohooks.terminal import Terminal

DESCRIPTION = "autohooks - Manage git hooks"


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version}",
    )

    subparsers = parser.add_subparsers(dest="command")
    activate_parser = subparsers.add_parser(
        "activate", help="Activate the pre-commit hook."
    )
    activate_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force activation of hook even if a hook already exists",
    )
    activate_parser.add_argument(
        "-m",
        "--mode",
        dest="mode",
        choices=[
            str(Mode.PYTHONPATH),
            str(Mode.PIPENV),
            str(Mode.POETRY),
        ],
        help="Mode for loading autohooks during hook execution. Either load "
        "autohooks from the PYTHON_PATH, via pipenv or via poetry.",
    )
    activate_parser.set_defaults(func=install_hooks)

    check_parser = subparsers.add_parser(
        "check", help="Check installed pre-commit hook"
    )
    check_parser.set_defaults(func=check_hooks)

    plugins_parser = subparsers.add_parser(
        "plugins", help="Manage autohooks plugins"
    )
    plugins_parser.set_defaults(func=plugins)

    plugins_subparsers = plugins_parser.add_subparsers(
        dest="subcommand", required=True
    )

    add_plugins_parser = plugins_subparsers.add_parser(
        "add", help="Add plugins."
    )
    add_plugins_parser.set_defaults(plugins_func=add_plugins)
    add_plugins_parser.add_argument("name", nargs="+", help="Plugin(s) to add")

    remove_plugins_parser = plugins_subparsers.add_parser(
        "remove", help="Remove plugins."
    )
    remove_plugins_parser.set_defaults(plugins_func=remove_plugins)
    remove_plugins_parser.add_argument(
        "name", nargs="+", help="Plugin(s) to remove"
    )

    list_plugins_parser = plugins_subparsers.add_parser(
        "list", help="List current used plugins."
    )
    list_plugins_parser.set_defaults(plugins_func=list_plugins)

    args = parser.parse_args()

    if not args.command:
        parser.print_usage()
        sys.exit(1)

    term = Terminal()
    args.func(term, args)


if __name__ == "__main__":
    main()
