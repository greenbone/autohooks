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

from autohooks.install import (
    get_pre_commit_hook_path,
    get_pre_commit_hook_template_path,
)

from autohooks.config import (
    get_pyproject_toml_path,
    load_config_from_pyproject_toml,
    AUTOHOOKS_SECTION,
)

from autohooks.precommit.run import (
    autohooks_module_path,
    load_plugin,
    has_precommit_function,
    has_precommit_parameters,
)

from autohooks.terminal import ok, error, warning


def check_hooks():
    pre_commit_hook = get_pre_commit_hook_path()
    pre_commit_template = get_pre_commit_hook_template_path()

    template = pre_commit_template.read_text()

    if pre_commit_hook.is_file():
        hook = pre_commit_hook.read_text()
        if hook == template:
            ok('autohooks pre-commit hook is active.')
        else:
            error(
                'autohooks pre-commit hook is not active. But a different '
                'pre-commit hook has been found at {}.'.format(
                    str(pre_commit_hook)
                )
            )

    else:
        error(
            'autohooks pre-commit hook not active. Please run \'autohooks '
            'activate\'.'
        )

    pyproject_toml = get_pyproject_toml_path()
    if not pyproject_toml.exists():
        error(
            'Missing {} file. Please add a pyproject.toml file and include '
            'a "{}" section.'.format(str(pyproject_toml), AUTOHOOKS_SECTION)
        )
    else:
        config = load_config_from_pyproject_toml(pyproject_toml)
        if not config.is_autohooks_enabled():
            error(
                'autohooks is not enabled in your {} file. Please add '
                'a "{}" section.'.format(str(pyproject_toml), AUTOHOOKS_SECTION)
            )
        else:
            plugins = config.get_pre_commit_script_names()
            if not plugins:
                error(
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
                                error(
                                    'Plugin "{}" has no precommit function. '
                                    'The function is required to run the '
                                    'plugin as git pre commit hook.'.format(
                                        name
                                    )
                                )
                            elif not has_precommit_parameters(plugin):
                                warning(
                                    'Plugin "{}" uses a deprecated signature '
                                    'for its precommit function. It is missing '
                                    'the **kwargs parameter.'.format(name)
                                )
                            else:
                                ok(
                                    'Plugin "{}" active and loadable'.format(
                                        name
                                    )
                                )
                        except ImportError as e:
                            error(
                                '"{}" is not a valid autohooks '
                                'plugin. {}'.format(name, e)
                            )
