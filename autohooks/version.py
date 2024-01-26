# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from autohooks.__version__ import __version__ as _current_version


def get_version() -> str:
    """
    Returns the current version of autohooks
    """
    return _current_version
