# Copyright (C) 2017-2019 Greenbone Networks GmbH
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

from .utils import get_project_root_path


class Config:

    def __init__(self, config_dict=None):
        self._config = config_dict

    def is_autohooks_enabled(self):
        return self._config is not None


def load_config_from_pyproject_toml():
    root = get_project_root_path()
    pyproject_toml = root / 'pyproject.toml'

    if not pyproject_toml.exists():
        return Config()

    config_dict = toml.load(str(pyproject_toml))
    autohooks_config = config_dict.get('tool', {}).get('autohooks')
    return Config(autohooks_config)
