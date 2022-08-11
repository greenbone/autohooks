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

from argparse import Namespace
from typing import Iterable

from autohooks.config import load_config_from_pyproject_toml
from autohooks.precommit.run import autohooks_module_path, check_plugin
from autohooks.settings import AutohooksSettings
from autohooks.terminal import Terminal
from autohooks.utils import get_pyproject_toml_path


def plugins(term: Terminal, args: Namespace) -> None:
    args.plugins_func(term, args)


def print_current_plugins(
    term: Terminal, current_plugins: Iterable[str]
) -> None:
    """
    Print the currently used plugins to the terminal
    """
    term.info("Currently used plugins:")
    with term.indent(), autohooks_module_path():
        if not current_plugins:
            term.print("None")
            return

        for plugin in sorted(current_plugins):
            result = check_plugin(plugin)
            if result:
                term.error(f'"{plugin}": {result}')
            else:
                term.ok(f'"{plugin}"')


# pylint: disable=unused-argument
def list_plugins(term: Terminal, args: Namespace) -> None:
    """
    CLI handler function to list the currently used plugins
    """
    pyproject_toml = get_pyproject_toml_path()
    config = load_config_from_pyproject_toml(pyproject_toml)

    current_plugins = (
        config.settings.pre_commit if config.has_autohooks_config() else []
    )
    print_current_plugins(term, current_plugins)


def add_plugins(term: Terminal, args: Namespace) -> None:
    """
    CLI handler function to add new plugins
    """
    pyproject_toml = get_pyproject_toml_path()
    config = load_config_from_pyproject_toml(pyproject_toml)
    plugins_to_add = set(args.name)

    if config.has_autohooks_config():
        settings = config.settings
        existing_plugins = set(settings.pre_commit)
        all_plugins = plugins_to_add | existing_plugins
        duplicate_plugins = plugins_to_add & existing_plugins
        new_plugins = plugins_to_add - existing_plugins
        settings.pre_commit = all_plugins

        if duplicate_plugins:
            term.info("Skipped already used plugins:")
            with term.indent():
                for plugin in sorted(duplicate_plugins):
                    term.warning(f'"{plugin}"')
    else:
        all_plugins = plugins_to_add
        new_plugins = plugins_to_add
        settings = AutohooksSettings(pre_commit=all_plugins)
        config.settings = settings

    settings.write(pyproject_toml)

    if new_plugins:
        term.info("Added plugins:")
        with term.indent():
            for plugin in sorted(new_plugins):
                term.ok(f'"{plugin}"')

    print_current_plugins(term, all_plugins)


def remove_plugins(term: Terminal, args: Namespace) -> None:
    """
    CLI handler function to remove plugins
    """
    pyproject_toml = get_pyproject_toml_path()
    config = load_config_from_pyproject_toml(pyproject_toml)
    plugins_to_remove = set(args.name)

    if config.has_autohooks_config():
        settings = config.settings
        existing_plugins = set(settings.pre_commit)
        removed_plugins = existing_plugins & plugins_to_remove
        all_plugins = existing_plugins - plugins_to_remove
        skipped_plugins = plugins_to_remove - existing_plugins
        settings.pre_commit = all_plugins

        if skipped_plugins:
            term.info("Skipped not used plugins:")
            with term.indent():
                for plugin in sorted(skipped_plugins):
                    term.warning(f'"{plugin}"')

        if removed_plugins:
            term.info("Removed plugins:")
            with term.indent():
                for plugin in sorted(removed_plugins):
                    term.ok(f'"{plugin}"')

        settings.write(pyproject_toml)

        print_current_plugins(term, all_plugins)
    else:
        term.warning("No plugins to remove.")
