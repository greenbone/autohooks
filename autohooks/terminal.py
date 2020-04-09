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

import shutil

from contextlib import contextmanager

from typing import Callable, Generator

import colorful as cf

TERMINAL_SIZE_FALLBACK = (80, 24)  # use a small standard size as fallback


class Terminal:
    def __init__(self):
        self._indent = 0

    @staticmethod
    def get_width() -> int:
        """
        Get the width of the terminal window
        """
        width, _ = shutil.get_terminal_size(TERMINAL_SIZE_FALLBACK)
        return width

    def _print_end(self, message: str, status: str, color: Callable) -> None:
        extra = 4  # '[ ' and ' ]'

        if self._indent > 0:
            message = ' ' * self._indent + message

        width = self.get_width()

        if width > 0:
            message += ' ' * (int(width) - len(message) - extra - len(status))

        print(
            message + '[', color(status), ']',
        )

    @contextmanager
    def indent(self, indentation: int = 4) -> Generator:
        current_indent = self._indent
        self.add_indent(indentation)

        yield self

        self._indent = current_indent

    def add_indent(self, indentation: int = 4) -> None:
        self._indent += indentation

    def reset_indent(self) -> None:
        self._indent = 0

    def print(self, *messages: str) -> None:
        msg = ''
        if self._indent > 0:
            msg = ' ' * (self._indent)
        msg += ' '.join(messages)
        print(msg)

    def ok(self, message: str) -> None:
        self._print_end(message, 'ok', cf.green)

    def fail(self, message: str) -> None:
        self._print_end(message, 'fail', cf.red)

    def error(self, message: str) -> None:
        self._print_end(message, 'error', cf.red)

    def warning(self, message: str) -> None:
        self._print_end(message, 'warning', cf.yellow)

    def info(self, message: str) -> None:
        self._print_end(message, 'info', cf.cyan)
