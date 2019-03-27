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

import toml

from autohooks.utils import get_pyproject_toml_path

AUTOHOOKS_SECTION = 'tool.autohooks'


class Config:
    def __init__(self, config_dict=None):
        self._config_dict = config_dict or {}

    def get(self, *keys):
        config_dict = self._config_dict

        for key in keys:
            config_dict = config_dict.get(key, {})

        return Config(config_dict)

    def get_value(self, key, default=None):
        return self._config_dict.get(key, default)

    def is_empty(self):
        return False if self._config_dict else True


class AutohooksConfig:
    def __init__(self, config_dict=None):
        self._config = Config(config_dict)
        self._autohooks_config = self._config.get('tool').get('autohooks')

    def has_config(self):
        return not self._config.is_empty()

    def has_autohooks_config(self):
        return not self._autohooks_config.is_empty()

    def is_autohooks_enabled(self):
        return self.has_autohooks_config()

    def get_pre_commit_script_names(self):
        if self.has_autohooks_config():
            return self._autohooks_config.get_value('pre-commit', [])

        return []

    def get_config(self):
        return self._config


def load_config_from_pyproject_toml(pyproject_toml=None):
    if pyproject_toml is None:
        pyproject_toml = get_pyproject_toml_path()

    if not pyproject_toml.exists():
        return AutohooksConfig()

    config_dict = toml.load(str(pyproject_toml))
    return AutohooksConfig(config_dict)
