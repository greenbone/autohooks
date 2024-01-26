# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable, Optional

import tomlkit


class Mode(Enum):
    PIPENV = 1
    PYTHONPATH = 2
    POETRY = 3
    PIPENV_MULTILINE = 4
    POETRY_MULTILINE = 5
    UNDEFINED = -1
    UNKNOWN = -2

    def get_effective_mode(self):
        if self.value == Mode.PIPENV.value:
            return Mode.PIPENV
        if self.value == Mode.PIPENV_MULTILINE.value:
            return Mode.PIPENV_MULTILINE
        if self.value == Mode.POETRY.value:
            return Mode.POETRY
        if self.value == Mode.POETRY_MULTILINE.value:
            return Mode.POETRY_MULTILINE
        return Mode.PYTHONPATH

    @staticmethod
    def from_string(modestring: Optional[str]) -> "Mode":
        if not modestring:
            return Mode.UNDEFINED

        try:
            return Mode[modestring.upper()]
        except KeyError:
            return Mode.UNKNOWN

    def __str__(self) -> str:
        return self.name.lower()  # pylint: disable=no-member


@dataclass
class AutohooksSettings:
    mode: Mode = Mode.UNDEFINED
    pre_commit: Iterable[str] = field(default_factory=list)

    def write(self, filename: Path) -> None:
        """
        Write the current AutohooksSettings to a TOML file

        If the TOML file already exists only the [tool.autohooks] section is
        overridden.
        """
        if filename.exists():
            toml_doc: tomlkit.TOMLDocument = tomlkit.loads(filename.read_text())
        else:
            toml_doc = tomlkit.document()

        if "tool" not in toml_doc:
            toml_doc["tool"] = tomlkit.table(is_super_table=True)
        if "autohooks" not in toml_doc["tool"]:  # type: ignore
            toml_doc["tool"]["autohooks"] = tomlkit.table()  # type: ignore

        config_dict = {
            "mode": str(self.mode.get_effective_mode()),
            "pre-commit": sorted(self.pre_commit),
        }

        toml_doc["tool"]["autohooks"].update(config_dict)  # type: ignore

        filename.write_text(tomlkit.dumps(toml_doc), encoding="utf8")
