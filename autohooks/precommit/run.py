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

import importlib
import inspect
import sys
from contextlib import contextmanager
from types import ModuleType
from typing import Generator, Optional

from autohooks.config import load_config_from_pyproject_toml
from autohooks.hooks import PreCommitHook
from autohooks.settings import Mode
from autohooks.terminal import Progress, Terminal, _set_terminal
from autohooks.utils import get_project_autohooks_plugins_path


@contextmanager
def autohooks_module_path() -> Generator:
    plugins = get_project_autohooks_plugins_path()
    plugins_dir_name = str(plugins)

    if plugins.is_dir():
        sys.path.append(plugins_dir_name)

    yield

    if plugins_dir_name in sys.path:
        sys.path.remove(plugins_dir_name)


def load_plugin(name: str) -> ModuleType:
    return importlib.import_module(name)


def has_precommit_function(plugin: ModuleType) -> bool:
    return hasattr(plugin, "precommit") and inspect.isfunction(plugin.precommit)


def has_precommit_parameters(plugin: ModuleType) -> bool:
    signature = inspect.signature(plugin.precommit)
    return bool(signature.parameters)


def check_hook_is_current(
    term: Terminal, pre_commit_hook: PreCommitHook
) -> None:
    if not pre_commit_hook.is_current_autohooks_pre_commit_hook():
        term.warning(
            "autohooks pre-commit hook is outdated. Please run "
            "'autohooks activate --force' to update your pre-commit "
            "hook."
        )


def check_hook_mode(term: Terminal, config_mode: Mode, hook_mode: Mode) -> None:
    if config_mode.get_effective_mode() != hook_mode.get_effective_mode():
        term.warning(
            f'autohooks mode "{str(hook_mode)}" in pre-commit hook differs '
            f'from mode "{str(config_mode)}" in pyproject.toml file.'
        )


class CheckPluginResult:
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class CheckPluginError(CheckPluginResult):
    """
    Raised if a plugin check failed
    """


class CheckPluginWarning(CheckPluginResult):
    """
    Used if a plugin check raises a warning
    """


def check_plugin(plugin_name: str) -> Optional[CheckPluginResult]:
    """
    Check if a plugin (Python module) is valid and can be used

    Returns:
        A CheckPluginResult in case of an issue with the plugin
    """
    try:
        plugin = load_plugin(plugin_name)
        if not has_precommit_function(plugin):
            return CheckPluginError(
                f'Plugin "{plugin_name}" has no precommit '
                "function. The function is required to run"
                " the plugin as git pre commit hook."
            )
        elif not has_precommit_parameters(plugin):
            return CheckPluginWarning(
                f'Plugin "{plugin_name}" uses a deprecated '
                "signature for its precommit function. It "
                "is missing the **kwargs parameter."
            )
    except ImportError as e:
        return CheckPluginError(
            f'"{plugin_name}" is not a valid autohooks plugin. {e}'
        )


class ReportProgress:
    """
    A class to report progress of a plugin
    """

    def __init__(self, progress: Progress, task_id: int) -> None:
        self._progress = progress
        self._task_id = task_id

    def init(self, total: int) -> None:
        """
        Init the progress with the total number to process

        Args:
            total: Most of the time this should be the number of files to
                process.
        """
        self._progress.update(self._task_id, total=total)

    def update(self, advance: Optional[int] = 1) -> None:
        """
        Update the number of already processed steps/items/files.

        This increases the progress indicator.

        Args:
            advance: Number of steps/items/files the progress advanced. By
                default 1.
        """
        self._progress.advance(self._task_id, advance)


def run() -> int:
    term = Terminal()

    _set_terminal(term)

    config = load_config_from_pyproject_toml()

    pre_commit_hook = PreCommitHook()

    check_hook_is_current(term, pre_commit_hook)

    if config.has_autohooks_config():
        check_hook_mode(term, config.get_mode(), pre_commit_hook.read_mode())

    plugins = get_project_autohooks_plugins_path()
    plugins_dir_name = str(plugins)

    if plugins.is_dir():
        sys.path.append(plugins_dir_name)

    term.bold_info("autohooks => pre-commit")

    with autohooks_module_path(), term.indent(), Progress(
        terminal=term
    ) as progress:
        for name in config.get_pre_commit_script_names():
            term.info(f"Running {name}")
            with term.indent():
                try:
                    plugin = load_plugin(name)
                    if not has_precommit_function(plugin):
                        term.fail(
                            f"No precommit function found in plugin {name}. "
                            "Your autohooks settings may be invalid."
                        )
                        return 1

                    task_id = progress.add_task(
                        f"Running {name}", total=None, name=name
                    )
                    report_progress = ReportProgress(progress, task_id)
                    if has_precommit_parameters(plugin):
                        retval = plugin.precommit(
                            config=config.get_config(),
                            report_progress=report_progress,
                        )
                    else:
                        term.warning(
                            "precommit function without kwargs is deprecated. "
                            f"Please update {name} to a newer version."
                        )
                        retval = plugin.precommit()

                    progress.finish_task(task_id)

                    if retval:
                        return retval

                except ImportError as e:
                    term.error(
                        "An error occurred while importing pre-commit "
                        f"hook {name}. {e}."
                    )
                    return 1
                except Exception as e:  # pylint: disable=broad-except
                    term.error(
                        "An error occurred while running pre-commit "
                        f"hook {name}. {e}."
                    )
                    return 1

    return 0
