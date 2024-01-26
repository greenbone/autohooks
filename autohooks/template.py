# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from pathlib import Path
from string import Template
from typing import Dict, Optional, Union

from autohooks.settings import Mode
from autohooks.utils import get_autohooks_directory_path

PYTHON3_SHEBANG = "/usr/bin/env python3"
PIPENV_SHEBANG = "/usr/bin/env -S pipenv run python3"
POETRY_SHEBANG = "/usr/bin/env -S poetry run python"
# For OS's that don't support '/usr/bin/env -S'.
PIPENV_MULTILINE_SHEBANG = (
    "/bin/sh\n"
    "\"true\" ''':'\n"
    'pipenv run python3 "$0" "$@"\n'
    'exit "$?"\n'
    "'''"
)
POETRY_MULTILINE_SHEBANG = (
    "/bin/sh\n"
    "\"true\" ''':'\n"
    'poetry run python "$0" "$@"\n'
    'exit "$?"\n'
    "'''"
)

TEMPLATE_VERSION = 1


def get_pre_commit_hook_template_path() -> Path:
    setup_dir_path = get_autohooks_directory_path()
    return setup_dir_path / "precommit" / "template"


class PreCommitTemplate:
    def __init__(self, template_path: Optional[Path] = None) -> None:
        if template_path is None:
            template_path = get_pre_commit_hook_template_path()
        self._load(template_path)

    def _load(self, template_path: Path) -> None:
        self._template = Template(template_path.read_text())

    def render(self, *, mode: Mode) -> str:
        mode = mode.get_effective_mode()

        params: Dict[str, Union[str, int]] = dict(VERSION=TEMPLATE_VERSION)

        if mode == Mode.PIPENV:
            params["SHEBANG"] = PIPENV_SHEBANG
        elif mode == Mode.POETRY:
            params["SHEBANG"] = POETRY_SHEBANG
        elif mode == Mode.PIPENV_MULTILINE:
            params["SHEBANG"] = PIPENV_MULTILINE_SHEBANG
        elif mode == Mode.POETRY_MULTILINE:
            params["SHEBANG"] = POETRY_MULTILINE_SHEBANG
        else:
            params["SHEBANG"] = PYTHON3_SHEBANG

        return self._template.safe_substitute(params)
