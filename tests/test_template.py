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

import unittest

from autohooks.settings import Mode
from autohooks.template import (
    PreCommitTemplate,
    get_pre_commit_hook_template_path,
)

DEFAULT_TEMPLATE = """#!/usr/bin/env python3
# meta = { version = 1 }

import sys

try:
    from autohooks.precommit import run
    sys.exit(run())
except ImportError:
    print(
        "Error: autohooks is not installed. To force creating a commit without "
        "verification via autohooks run 'git commit --no-verify'.",
        file=sys.stderr,
    )
    sys.exit(1)
"""


class FakeTemplatePath:
    def __init__(self, text):
        self._text = text

    def read_text(self):
        return self._text


class PreCommitTemplateTestCase(unittest.TestCase):
    def test_should_use_default_template(self):
        template = PreCommitTemplate()
        self.assertEqual(
            template.render(mode=Mode.PYTHONPATH), DEFAULT_TEMPLATE
        )

    def test_should_render_mode_pipenv(self):
        path = FakeTemplatePath("$SHEBANG")
        template = PreCommitTemplate(path)
        self.assertEqual(
            template.render(mode=Mode.PIPENV),
            "/usr/bin/env -S pipenv run python3",
        )

    def test_should_render_mode_poetry(self):
        path = FakeTemplatePath("$SHEBANG")
        template = PreCommitTemplate(path)
        self.assertEqual(
            template.render(mode=Mode.POETRY),
            "/usr/bin/env -S poetry run python3",
        )

    def test_should_render_mode_pipenv_multiline(self):
        path = FakeTemplatePath("$SHEBANG")
        template = PreCommitTemplate(path)
        self.assertEqual(
            template.render(mode=Mode.PIPENV_MULTILINE),
            (
                "/bin/sh\n"
                "\"true\" ''':'\n"
                "pipenv run python3 \"$0\" \"$@\"\n"
                "exit \"$?\"\n"
                "'''"
            ),
        )

    def test_should_render_mode_poetry_multiline(self):
        path = FakeTemplatePath("$SHEBANG")
        template = PreCommitTemplate(path)
        self.assertEqual(
            template.render(mode=Mode.POETRY_MULTILINE),
            (
                "/bin/sh\n"
                "\"true\" ''':'\n"
                "poetry run python3 \"$0\" \"$@\"\n"
                "exit \"$?\"\n"
                "'''"
            ),
        )

    def test_should_render_mode_unknown(self):
        path = FakeTemplatePath("$SHEBANG")
        template = PreCommitTemplate(path)
        self.assertEqual(
            template.render(mode=Mode.UNDEFINED), "/usr/bin/env python3"
        )

    def test_should_render_mode_undefined(self):
        path = FakeTemplatePath("$SHEBANG")
        template = PreCommitTemplate(path)
        self.assertEqual(
            template.render(mode=Mode.UNDEFINED), "/usr/bin/env python3"
        )


class GetPreCommitHookTemplatePath(unittest.TestCase):
    def test_template_exists(self):
        template_path = get_pre_commit_hook_template_path()
        self.assertTrue(template_path.exists())
        self.assertTrue(template_path.is_file())


if __name__ == '__main__':
    unittest.main()
