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

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import tomlkit

from autohooks.settings import AutohooksSettings, Mode
from autohooks.utils import get_pyproject_toml_path, is_split_env

AUTOHOOKS_SECTION = "tool.autohooks"


class Config:
    def __init__(self, config_dict: Dict = None) -> None:
        self._config_dict = config_dict or {}

    def get(self, *keys: str) -> "Config":
        config_dict = self._config_dict

        for key in keys:
            config_dict = config_dict.get(key, {}).copy()

        return Config(config_dict)

    def get_value(self, key: str, default: Any = None) -> Union[str, List[str]]:
        return self._config_dict.get(key, default)

    def is_empty(self) -> bool:
        return not bool(self._config_dict)


def _gather_mode(mode: Optional[str]) -> Mode:
    """
    Gather the mode from a mode string
    """
    mode = Mode.from_string(mode)
    is_virtual_env = mode == Mode.PIPENV or mode == Mode.POETRY
    if is_virtual_env and not is_split_env():
        if mode == Mode.POETRY:
            mode = Mode.POETRY_MULTILINE
        else:
            mode = Mode.PIPENV_MULTILINE
    return mode


class AutohooksConfig:
    def __init__(
        self,
        *,
        settings: Optional[AutohooksSettings] = None,
        config: Optional[Config] = None,
    ) -> None:
        self.config = Config() if config is None else config
        self.settings = settings

    def get_config(self) -> Config:
        return self.config

    def has_autohooks_config(self) -> bool:
        return self.settings is not None

    def get_pre_commit_script_names(self) -> List[str]:
        return self.settings.pre_commit if self.has_autohooks_config() else []

    def get_mode(self) -> Mode:
        return (
            self.settings.mode
            if self.has_autohooks_config()
            else Mode.UNDEFINED
        )

    @staticmethod
    def from_dict(config_dict: Dict[str, Any]) -> "AutohooksConfig":
        """
        Create a new AutohooksConfig from a dictionary

        Args:
            config_data: A dictionary containing the config data

        Returns:
            A new AutohooksConfig
        """
        config = Config(config_dict)
        autohooks_dict = config.get("tool", "autohooks")
        if autohooks_dict.is_empty():
            settings = None
        else:
            settings = AutohooksSettings(
                mode=_gather_mode(autohooks_dict.get_value("mode")),
                pre_commit=autohooks_dict.get_value("pre-commit", []),
            )
        return AutohooksConfig(settings=settings, config=config)

    @staticmethod
    def from_toml(toml_file: Path) -> "AutohooksConfig":
        """
        Load an AutohooksConfig from a TOML file

        Args:
            toml_file: Path for the toml file to load

        Returns:
            A new AutohooksConfig
        """
        config_dict = tomlkit.loads(toml_file.read_text())
        return AutohooksConfig.from_dict(config_dict)


def load_config_from_pyproject_toml(
    pyproject_toml: Path = None,
) -> AutohooksConfig:
    """
    Load an AutohooksConfig from a pyproject.toml file

    If no path to the pyproject.toml file is passed the path will be determined
    from the current working directory and the project.

    Args:
        pyproject_toml: Path to the pyproject.toml file.

    Returns:
        A new AutohooksConfig
    """
    if pyproject_toml is None:
        pyproject_toml = get_pyproject_toml_path()

    if not pyproject_toml.exists():
        return AutohooksConfig()

    return AutohooksConfig.from_toml(pyproject_toml)
