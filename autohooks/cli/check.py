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

from pathlib import Path

from autohooks.config import (
    get_pyproject_toml_path,
    load_config_from_pyproject_toml,
    AUTOHOOKS_SECTION,
)

from autohooks.hooks import PreCommitHook

from autohooks.precommit.run import (
    autohooks_module_path,
    load_plugin,
    has_precommit_function,
    has_precommit_parameters,
)

from autohooks.settings import Mode

from autohooks.terminal import Terminal


def check_hooks(term: Terminal) -> None:
    pre_commit_hook = PreCommitHook()
    check_pre_commit_hook(term, pre_commit_hook)

    pyproject_toml = get_pyproject_toml_path()

    check_config(term, pyproject_toml, pre_commit_hook)


def check_pre_commit_hook(
    term: Terminal, pre_commit_hook: PreCommitHook
) -> None:
    if pre_commit_hook.exists():
        if pre_commit_hook.is_autohooks_pre_commit_hook():
            term.ok('autohooks pre-commit hook is active.')

            if pre_commit_hook.is_current_autohooks_pre_commit_hook():
                term.ok('autohooks pre-commit hook is up-to-date.')
            else:
                term.warning(
                    'autohooks pre-commit hook is outdated. Please run '
                    '\'autohooks activate --force\' to update your pre-commit '
                    'hook.'
                )

            hook_mode = pre_commit_hook.read_mode()
            if hook_mode == Mode.UNKNOWN:
                term.warning(
                    'Unknown autohooks mode in {}. Falling back to "{}" '
                    'mode.'.format(
                        str(pre_commit_hook),
                        str(hook_mode.get_effective_mode()),
                    )
                )
        else:
            term.error(
                'autohooks pre-commit hook is not active. But a different '
                'pre-commit hook has been found at {}.'.format(
                    str(pre_commit_hook)
                )
            )

    else:
        term.error(
            'autohooks pre-commit hook not active. Please run \'autohooks '
            'activate\'.'
        )


def check_config(
    term: Terminal,
    pyproject_toml: Path,
    pre_commit_hook: PreCommitHook,
) -> None:
    if not pyproject_toml.exists():
        term.error(
            'Missing {} file. Please add a pyproject.toml file and include '
            'a "{}" section.'.format(str(pyproject_toml), AUTOHOOKS_SECTION)
        )
    else:
        config = load_config_from_pyproject_toml(pyproject_toml)
        if not config.is_autohooks_enabled():
            term.error(
                'autohooks is not enabled in your {} file. Please add '
                'a "{}" section.'.format(str(pyproject_toml), AUTOHOOKS_SECTION)
            )
        elif pre_commit_hook.exists():
            config_mode = config.get_mode()
            hook_mode = pre_commit_hook.read_mode()

            if config_mode == Mode.UNDEFINED:
                term.warning(
                    'autohooks mode is not defined in {}.'.format(
                        str(pyproject_toml)
                    )
                )
            elif config_mode == Mode.UNKNOWN:
                term.warning(
                    'Unknown autohooks mode in {}.'.format(str(pyproject_toml))
                )

            if (
                config_mode.get_effective_mode()
                != hook_mode.get_effective_mode()
            ):
                term.warning(
                    'autohooks mode "{}" in pre-commit hook {} differs from '
                    'mode "{}" in {}.'.format(
                        str(hook_mode),
                        str(pre_commit_hook),
                        str(config_mode),
                        str(pyproject_toml),
                    )
                )

            term.info(
                'Using autohooks mode "{}".'.format(
                    str(hook_mode.get_effective_mode())
                )
            )

            plugins = config.get_pre_commit_script_names()
            if not plugins:
                term.error(
                    'No autohooks plugin is activated in {} for your pre '
                    'commit hook. Please add a '
                    '"pre-commit = [plugin1, plugin2]" '
                    'setting.'.format(str(pyproject_toml))
                )
            else:
                with autohooks_module_path():
                    for name in plugins:
                        try:
                            plugin = load_plugin(name)
                            if not has_precommit_function(plugin):
                                term.error(
                                    'Plugin "{}" has no precommit function. '
                                    'The function is required to run the '
                                    'plugin as git pre commit hook.'.format(
                                        name
                                    )
                                )
                            elif not has_precommit_parameters(plugin):
                                term.warning(
                                    'Plugin "{}" uses a deprecated signature '
                                    'for its precommit function. It is missing '
                                    'the **kwargs parameter.'.format(name)
                                )
                            else:
                                term.ok(
                                    'Plugin "{}" active and loadable.'.format(
                                        name
                                    )
                                )
                        except ImportError as e:
                            term.error(
                                '"{}" is not a valid autohooks '
                                'plugin. {}'.format(name, e)
                            )
