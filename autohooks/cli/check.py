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

from ..install import (
    install_pre_commit_hook,
    get_pre_commit_hook_path,
    get_pre_commit_hook_template_path,
)


def check_hooks():
    pre_commit_hook = get_pre_commit_hook_path()
    pre_commit_template = get_pre_commit_hook_template_path()

    template = pre_commit_template.read_text()

    if pre_commit_hook.is_file():
        hook = pre_commit_hook.read_text()
        if hook == template:
            print('autohooks pre-commit hook is active.')
        else:
            print(
                'autohooks pre-commit hook is not active. But a different '
                'pre-commit hook has been found at {}.'.format(
                    str(pre_commit_hook)
                )
            )

    else:
        print(
            'autohooks pre-commit hook not active. Please run \'autohooks '
            'activate\'.'
        )
