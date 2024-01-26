# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Main Plugin API
"""

from autohooks.config import Config
from autohooks.precommit.run import ReportProgress
from autohooks.terminal import bold_info, error, fail, info, ok, out, warning

__all__ = [
    "Config",
    "ReportProgress",
    "error",
    "fail",
    "info",
    "bold_info",
    "ok",
    "out",
    "warning",
]
