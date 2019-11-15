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

import importlib
import inspect
import sys

from types import ModuleType
from typing import Generator

from contextlib import contextmanager

from autohooks.config import load_config_from_pyproject_toml
from autohooks.hooks import PreCommitHook
from autohooks.settings import Mode
from autohooks.terminal import error, warning
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
    return hasattr(plugin, 'precommit') and inspect.isfunction(plugin.precommit)


def has_precommit_parameters(plugin: ModuleType) -> bool:
    signature = inspect.signature(plugin.precommit)
    return bool(signature.parameters)


def check_hook_is_current(pre_commit_hook: PreCommitHook):
    if not pre_commit_hook.is_current_autohooks_pre_commit_hook():
        warning(
            'autohooks pre-commit hook is outdated. Please run '
            '\'autohooks activate --force\' to update your pre-commit '
            'hook.'
        )


def check_hook_mode(config_mode: Mode, hook_mode: Mode) -> None:
    if config_mode != hook_mode:
        warning(
            'autohooks mode in pre-commit hook ("{}") differs from '
            'mode in pyproject.toml file ("{}"). Please run \'autohooks '
            'activate --force\' to enforce {} mode.'.format(
                str(hook_mode), str(config_mode), str(config_mode)
            )
        )


def run() -> int:
    print('autohooks => pre-commit')

    config = load_config_from_pyproject_toml()

    pre_commit_hook = PreCommitHook()

    check_hook_is_current(pre_commit_hook)
    check_hook_mode(config.get_mode(), pre_commit_hook.read_mode())

    plugins = get_project_autohooks_plugins_path()
    plugins_dir_name = str(plugins)

    if plugins.is_dir():
        sys.path.append(plugins_dir_name)

    with autohooks_module_path():
        for name in config.get_pre_commit_script_names():
            try:
                plugin = load_plugin(name)
                if not has_precommit_function(plugin):
                    error(
                        'No precommit function found in plugin {}. '
                        'Your autohooks settings may be invalid.'.format(name)
                    )
                    return 1

                if has_precommit_parameters(plugin):
                    retval = plugin.precommit(config=config.get_config())
                else:
                    warning(
                        'precommit function without kwargs is deprecated. '
                        'Please update {} to a newer version.'.format(name)
                    )
                    retval = plugin.precommit()

                if retval:
                    return retval

            except ImportError as e:
                error(
                    'An error occurred while importing pre-commit '
                    'hook {}. {}.'.format(name, e)
                )
                return 1
            except Exception as e:  # pylint: disable=broad-except
                error(
                    'An error occurred while running pre-commit '
                    'hook {}. {}.'.format(name, e)
                )
                return 1

    return 0
