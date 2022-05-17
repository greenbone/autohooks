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

import fnmatch
import os
from os import PathLike
from pathlib import Path
from typing import Iterable


def is_python_path(path: Path) -> bool:
    if not path:
        return False
    return path.match("*.py")


def match(path: PathLike, pattern_list: Iterable) -> bool:
    """
    Check if a Path matches to one of the patterns

    Internally fnmatch is used.
    See https://docs.python.org/3/library/fnmatch.html for details.

    Arguments:
        path (Path): Path to check if it matches to one of the patterns
        pattern_list (iterable): Iterable (e.g tuple or list) of patterns to
            match against the path

    Returns:
        Boolean: True if path matches a pattern of the list
    """
    for pattern in pattern_list:
        if fnmatch.fnmatch(os.fspath(path), pattern):
            return True
    return False
