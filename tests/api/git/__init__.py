# Copyright (C) 2022 Greenbone Networks GmbH
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
import random
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from autohooks.utils import exec_git


def randbytes(n: int) -> bytes:  # pylint: disable=invalid-name
    if hasattr(random, "randbytes"):
        return random.randbytes(n)
    return random.getrandbits(n * 8).to_bytes(n, "little")


def git_add(*paths: Path) -> None:
    exec_git("add", *paths)


def git_rm(*paths: Path) -> None:
    exec_git("rm", *paths)


def git_mv(from_path: Path, to_path: Path) -> None:
    exec_git("mv", from_path, to_path)


def git_commit(message: str = "Foo Bar"):
    exec_git("commit", "--no-gpg-sign", "-m", message)


class GitTestCase(unittest.TestCase):
    pass
