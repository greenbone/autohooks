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

from contextlib import contextmanager

from typing import Callable, Generator

import colorful as cf


class Terminal:
    def __init__(self):
        self._width = 0
        self._indent = 0

    def _check_size(self):
        self._width, _ = os.get_terminal_size()

    def _print_end(self, message: str, status: str, color: Callable) -> None:
        extra = 6  # '[ ', ' ]'
        # python is adding a ' ' between strings if used
        # in print('foo', 'bar', 'baz') is printed to "foo bar baz"
        if self._indent > 0:
            message = ' ' * self._indent + message
        self._check_size()
        print(
            message,
            ' ' * (int(self._width) - len(message) - extra - len(status)),
            '[',
            color(status),
            ']',
        )

    @contextmanager
    def indent(self, indentation: int = 4) -> Generator:
        current_indent = self._indent
        self.add_indent(indentation)

        yield self

        self._indent = current_indent

    def add_indent(self, indentation: int = 4) -> None:
        self._indent += indentation

    def print(self, *messages: str) -> None:
        print(messages)

    def ok(self, message: str) -> None:
        self._print_end(message, 'ok', cf.green)  # pylint: disable=no-member

    def fail(self, message: str) -> None:
        self._print_end(message, 'fail', cf.red)  # pylint: disable=no-member

    def error(self, message: str) -> None:
        self._print_end(message, 'error', cf.red)  # pylint: disable=no-member

    def warning(self, message: str) -> None:
        self._print_end(
            message, 'warning', cf.yellow  # pylint: disable=no-member
        )

    def info(self, message: str) -> None:
        self._print_end(message, 'info', cf.cyan)  # pylint: disable=no-member
