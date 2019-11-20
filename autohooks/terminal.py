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
import curses

from contextlib import contextmanager

from typing import Callable, Generator

from blessings import Terminal as Term


class Terminal:
    def __init__(self):
        self._indent = 0
        try:
            self._term = Term()
        except curses.error:
            # handle issues with terminals and force not to style anything
            # should not be necessary with blessings > 1.7 anymore
            self._term = Term(force_styling=None)

    def _print_end(self, message: str, status: str, color: Callable) -> None:
        width = self._term.width - 1
        extra = 4  # '[ ', ' ]'
        with self._term.location():
            self.print(
                message,
                self._term.move_x(width - extra - len(status)),
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
        with self._term.location(x=self._indent):
            print(*messages)

    def ok(self, message: str) -> None:
        self._print_end(message, 'ok', self._term.green)

    def fail(self, message: str) -> None:
        self._print_end(message, 'fail', self._term.red)

    def error(self, message: str) -> None:
        self._print_end(message, 'error', self._term.red)

    def warning(self, message: str) -> None:
        self._print_end(message, 'warning', self._term.yellow)

    def info(self, message: str) -> None:
        self._print_end(message, 'info', self._term.cyan)
