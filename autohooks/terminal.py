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

from blessings import Terminal

try:
    term = Terminal()  # pylint: disable=invalid-name
except curses.error:
    # handle issues with terminals and force not to style anything
    # should not be necessary with blessings > 1.7 anymore
    term = Terminal(force_styling=None)  # pylint: disable=invalid-name


def ok(message):
    print(message, '[', term.green('ok'), ']')


def fail(message):
    print(message, '[', term.red('fail'), ']')


def error(message):
    print(message, '[', term.red('error'), ']')


def warning(message):
    print(message, '[', term.yellow('warning'), ']')
