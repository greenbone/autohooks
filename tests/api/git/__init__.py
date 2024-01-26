# SPDX-FileCopyrightText: 2022-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import random
import unittest
from pathlib import Path

from autohooks.utils import exec_git


def randbytes(n: int) -> bytes:  # pylint: disable=invalid-name
    if hasattr(random, "randbytes"):
        return random.randbytes(n)
    return random.getrandbits(n * 8).to_bytes(n, "little")


def git_add(*paths: Path) -> None:
    exec_git("add", *paths)  # type: ignore[arg-type]


def git_rm(*paths: Path) -> None:
    exec_git("rm", *paths)  # type: ignore[arg-type]


def git_mv(from_path: Path, to_path: Path) -> None:
    exec_git("mv", from_path, to_path)  # type: ignore[arg-type]


def git_commit(message: str = "Foo Bar"):
    exec_git("commit", "--no-gpg-sign", "-m", message)


class GitTestCase(unittest.TestCase):
    pass
