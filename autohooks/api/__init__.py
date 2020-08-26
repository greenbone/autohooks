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
import colorful as cf

from autohooks.terminal import Terminal

__term = None  # pylint: disable=invalid-name

__all__ = [
    'error',
    'fail',
    'info',
    'bold_info',
    'ok',
    'out',
    'warning',
]


def ok(message: str) -> None:
    __term.ok(message)


def fail(message: str) -> None:
    __term.fail(message)


def error(message: str) -> None:
    __term.error(message)


def warning(message: str) -> None:
    __term.warning(message)


def info(message: str) -> None:
    __term.info(message)


def bold_info(message: str) -> None:
    __term.bold_info(message)


def out(message: str):
    __term.print(message)


def _set_terminal(term: Terminal):
    global __term  # pylint: disable=global-statement, invalid-name
    __term = term
