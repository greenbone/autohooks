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


import unittest
from argparse import Namespace
from unittest.mock import MagicMock, call

from autohooks.cli.activate import install_hooks
from tests import tempgitdir

CONFIG = """
[tool.autohooks]
mode = "poetry"
"""


class ActivateCliTestCase(unittest.TestCase):
    def test_install_hooks(self):
        with tempgitdir() as tmpdir:
            pyproject_toml = tmpdir / "pyproject.toml"
            pyproject_toml.write_text(CONFIG, encoding="utf8")

            term = MagicMock()
            args = Namespace(force=False, mode=None)

            install_hooks(term, args)

            term.warning.assert_not_called()
            term.ok.assert_called_once_with(
                f"autohooks pre-commit hook installed at {tmpdir}/"
                ".git/hooks/pre-commit using poetry mode."
            )

    def test_install_exists(self):
        with tempgitdir() as tmpdir:
            pyproject_toml = tmpdir / "pyproject.toml"
            pyproject_toml.write_text(CONFIG, encoding="utf8")
            pre_commit = tmpdir / ".git" / "hooks" / "pre-commit"
            pre_commit.touch()

            term = MagicMock()
            args = Namespace(force=False, mode=None)

            install_hooks(term, args)

            term.ok.assert_not_called()
            term.warning.assert_called_once_with(
                f"autohooks pre-commit hook is already installed at {tmpdir}/"
                ".git/hooks/pre-commit."
            )
            term.info.assert_has_calls(
                (
                    call(
                        "Run 'autohooks activate --force' to override the "
                        "current installed pre-commit hook."
                    ),
                    call(
                        "Run 'autohooks check' to validate the current status "
                        "of the installed pre-commit hook."
                    ),
                )
            )

    def test_install_hooks_force(self):
        with tempgitdir() as tmpdir:
            pyproject_toml = tmpdir / "pyproject.toml"
            pyproject_toml.write_text(CONFIG, encoding="utf8")
            pre_commit = tmpdir / ".git" / "hooks" / "pre-commit"
            pre_commit.touch()

            term = MagicMock()
            args = Namespace(force=True, mode=None)

            install_hooks(term, args)

            term.warning.assert_not_called()
            term.ok.assert_has_calls(
                (
                    call(f"autohooks settings written to {pyproject_toml}."),
                    call(
                        f"autohooks pre-commit hook installed at {pre_commit}"
                        " using poetry mode."
                    ),
                )
            )

    def test_install_no_config(self):
        with tempgitdir() as tmpdir:
            term = MagicMock()
            args = Namespace(force=False, mode=None)

            install_hooks(term, args)

            term.warning.assert_not_called()
            term.ok.assert_has_calls(
                (
                    call(
                        "autohooks settings written to "
                        f"{tmpdir}/pyproject.toml."
                    ),
                    call(
                        f"autohooks pre-commit hook installed at {tmpdir}/"
                        ".git/hooks/pre-commit using pythonpath mode."
                    ),
                )
            )

    def test_install_hooks_with_mode(self):
        with tempgitdir() as tmpdir:
            pyproject_toml = tmpdir / "pyproject.toml"
            pyproject_toml.write_text(CONFIG, encoding="utf8")

            term = MagicMock()
            args = Namespace(force=False, mode="pythonpath")

            install_hooks(term, args)

            term.warning.assert_not_called()
            term.ok.assert_called_once_with(
                f"autohooks pre-commit hook installed at {tmpdir}/"
                ".git/hooks/pre-commit using pythonpath mode."
            )
