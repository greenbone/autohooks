# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from argparse import Namespace

from autohooks.config import (
    get_pyproject_toml_path,
    load_config_from_pyproject_toml,
)
from autohooks.hooks import PreCommitHook
from autohooks.settings import AutohooksSettings, Mode
from autohooks.terminal import Terminal


def install_hooks(term: Terminal, args: Namespace) -> None:
    pre_commit_hook = PreCommitHook()
    pyproject_toml = get_pyproject_toml_path()
    config = load_config_from_pyproject_toml(pyproject_toml)

    if pre_commit_hook.exists() and not args.force:
        term.warning(
            "autohooks pre-commit hook is already"
            f" installed at {pre_commit_hook}."
        )
        with term.indent():
            term.print()
            term.info(
                "Run 'autohooks activate --force' to override the current "
                "installed pre-commit hook."
            )
            term.info(
                "Run 'autohooks check' to validate the current status of "
                "the installed pre-commit hook."
            )
    else:
        if args.mode:
            mode = Mode.from_string(args.mode)
        else:
            mode = config.get_mode().get_effective_mode()

        if not config.has_autohooks_config():
            settings = AutohooksSettings(mode=mode)
            config.settings = settings
            settings.write(pyproject_toml)

            term.ok(f"autohooks settings written to {pyproject_toml}.")
        elif args.force:
            settings = config.settings  # type: ignore
            settings.mode = mode
            settings.write(pyproject_toml)

            term.ok(f"autohooks settings written to {pyproject_toml}.")

        pre_commit_hook.write(mode=mode)

        term.ok(
            f"autohooks pre-commit hook installed at {pre_commit_hook}"
            f" using {mode} mode."
        )
