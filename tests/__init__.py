# -*- coding: utf-8 -*-
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
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from autohooks.utils import exec_git


@contextmanager
def tempdir(change_into=False) -> Generator[Path, None, None]:
    temp_dir = tempfile.TemporaryDirectory()

    if change_into:
        os.chdir(temp_dir.name)

    yield Path(temp_dir.name)

    temp_dir.cleanup()


@contextmanager
def tempgitdir() -> Generator[Path, None, None]:
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name)

    os.chdir(str(temp_path))

    exec_git("init", "-b", "main")
    exec_git("config", "--local", "user.email", "max.mustermann@example.com")
    exec_git("config", "--local", "user.name", "Max Mustermann")

    yield temp_path

    temp_dir.cleanup()
