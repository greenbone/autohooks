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

import argparse

from autohooks.version import get_version

from autohooks.cli.activate import install_hooks
from autohooks.cli.check import check_hooks

DESCRIPTION = 'autohooks - Manage git hooks'


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(get_version()),
    )

    subparsers = parser.add_subparsers(dest='command')
    activate_parser = subparsers.add_parser(
        'activate', help='Activate the pre-commit hook.'
    )
    activate_parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='Force activation of hook even if a hook already exists',
    )

    subparsers.add_parser('check', help='Check installed pre-commit hook')

    args = parser.parse_args()

    if not args.command:
        parser.print_usage()

    if args.command == 'activate':
        install_hooks(args)
    elif args.command == 'check':
        check_hooks()


if __name__ == "__main__":
    main()
