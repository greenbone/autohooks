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

from enum import Enum


class Mode(Enum):
    PIPENV = 1
    PYTHONPATH = 2
    POETRY = 3
    PIPENV_MULTILINE = 4
    POETRY_MULTILINE = 5
    UNDEFINED = -1
    UNKNOWN = -2

    def get_effective_mode(self):
        # pylint: disable=comparison-with-callable
        if self.value == Mode.PIPENV.value:
            return Mode.PIPENV
        if self.value == Mode.PIPENV_MULTILINE.value:
            return Mode.PIPENV_MULTILINE
        if self.value == Mode.POETRY.value:
            return Mode.POETRY
        if self.value == Mode.POETRY_MULTILINE.value:
            return Mode.POETRY_MULTILINE
        return Mode.PYTHONPATH

    @staticmethod
    def from_string(modestring: str) -> 'Mode':
        if not modestring:
            return Mode.UNDEFINED

        try:
            return Mode[modestring.upper()]
        except KeyError:
            return Mode.UNKNOWN

    def __str__(self) -> str:
        return self.name.lower()  # pylint: disable=no-member
