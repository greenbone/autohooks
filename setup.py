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

# pylint: disable=wrong-import-position, invalid-name

import sys

if sys.version_info[0] < 3:
    raise Exception('Python 2 is not supported by autohooks.')

from pathlib import Path

from setuptools import setup, find_namespace_packages

__here__ = Path(__file__).parent.resolve()

sys.path.insert(0, str(__here__))

from autohooks.config import PoetryConfig
from autohooks.install import PostInstall, PostDevelop


with (__here__ / 'README.md').open('r') as f:
    long_description = f.read()

config = PoetryConfig.from_pyproject_toml(__here__ / "pyproject.toml")

setup(
    name=config.get_name(),
    version=config.get_version(),
    author='Greenbone Networks GmbH',
    author_email='info@greenbone.net',
    description=config.get_description(),
    license=config.get_license(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=config.get_homepage(),
    packages=find_namespace_packages(include=['autohooks', 'autohooks.*']),
    package_data={'': ['template']},
    include_package_data=True,
    python_requires='>=3.5',
    classifiers=config.get_classifiers(),
    install_requires=['toml', 'colorful'],
    cmdclass={"install": PostInstall, "develop": PostDevelop},
    entry_points={
        'console_scripts': [
            '{}={}'.format(key, value)
            for key, value in config.get_scripts().items()
        ]
    },
)
