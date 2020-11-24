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

from pathlib import Path

from autohooks.config import (
    AutohooksConfig,
    Config,
    Mode,
    load_config_from_pyproject_toml,
)


def get_test_config_path(name):
    return Path(__file__).parent / name


class AutohooksConfigTestCase(unittest.TestCase):
    def test_load_from_toml_file(self):
        config_path = get_test_config_path('pyproject.test1.toml')
        self.assertTrue(config_path.is_file())

        config = load_config_from_pyproject_toml(config_path)

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())

        self.assertListEqual(
            config.get_pre_commit_script_names(), ['foo', 'bar']
        )

    def test_load_from_non_existing_toml_file(self):
        config_path = Path('foo')
        self.assertFalse(config_path.exists())

        config = load_config_from_pyproject_toml(config_path)

        self.assertFalse(config.has_config())
        self.assertFalse(config.has_autohooks_config())
        self.assertFalse(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.UNDEFINED)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_empty_config(self):
        config = AutohooksConfig()

        self.assertFalse(config.has_config())
        self.assertFalse(config.has_autohooks_config())
        self.assertFalse(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.UNDEFINED)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_empty_config_dict(self):
        config = AutohooksConfig({'foo': 'bar'})

        self.assertTrue(config.has_config())
        self.assertFalse(config.has_autohooks_config())
        self.assertFalse(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.UNDEFINED)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_missing_pre_commit(self):
        config = AutohooksConfig({'tool': {'autohooks': {'foo': 'bar'}}})

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.UNDEFINED)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_mode_pipenv(self):
        config = AutohooksConfig({'tool': {'autohooks': {'mode': 'pipenv'}}})

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.PIPENV)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_mode_pipenv_multiline(self):
        config = AutohooksConfig(
            {'tool': {'autohooks': {'mode': 'pipenv_multiline'}}}
        )

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.PIPENV_MULTILINE)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_mode_poetry(self):
        config = AutohooksConfig({'tool': {'autohooks': {'mode': 'poetry'}}})

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.POETRY)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_mode_poetry_multiline(self):
        config = AutohooksConfig(
            {'tool': {'autohooks': {'mode': 'poetry_multiline'}}}
        )

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.POETRY_MULTILINE)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_mode_pythonpath(self):
        config = AutohooksConfig(
            {'tool': {'autohooks': {'mode': 'pythonpath'}}}
        )

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.PYTHONPATH)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_mode_unknown(self):
        config = AutohooksConfig({'tool': {'autohooks': {'mode': 'foo'}}})

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.UNKNOWN)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_mode_undefined(self):
        config = AutohooksConfig({'tool': {'autohooks': {'mode': None}}})

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertTrue(config.is_autohooks_enabled())
        self.assertEqual(config.get_mode(), Mode.UNDEFINED)

        self.assertEqual(len(config.get_pre_commit_script_names()), 0)

    def test_get_config_dict(self):
        config_in = {'tool': {'autohooks': {'lorem': 'ipsum'}}, 'foo': 'bar'}
        config = AutohooksConfig(config_in)

        self.assertTrue(config.has_config())
        self.assertTrue(config.has_autohooks_config())
        self.assertEqual(config.get_mode(), Mode.UNDEFINED)

        config_out = config.get_config()

        self.assertEqual(config_out.get_value('foo'), 'bar')

    def test_load_config_dict_from_toml_file(self):
        config_path = get_test_config_path('pyproject.test2.toml')
        self.assertTrue(config_path.is_file())

        autohooksconfig = load_config_from_pyproject_toml(config_path)
        self.assertTrue(autohooksconfig.has_config())

        config = autohooksconfig.get_config()
        self.assertEqual(
            config.get('tool')
            .get('autohooks')
            .get('plugins')
            .get('foo')
            .get_value('bar'),
            'ipsum',
        )
        self.assertEqual(
            config.get('tool')
            .get('autohooks')
            .get('plugins')
            .get('foo')
            .get_value('lorem'),
            'dolor',
        )
        self.assertEqual(
            config.get('tool')
            .get('autohooks')
            .get('plugins')
            .get('bar')
            .get_value('foo'),
            'bar',
        )


class ConfigTestCase(unittest.TestCase):
    def test_empty_config(self):
        config = Config()

        self.assertTrue(config.is_empty())

        bar_config = config.get('foo').get('bar')
        self.assertTrue(bar_config.is_empty())

        self.assertTrue(config.get_value('foo', True))
        self.assertListEqual(config.get_value('foo', ['a']), ['a'])

    def test_config_dict(self):
        config_dict = {
            'tool': {'autohooks': {'lorem': 'ipsum'}},
            'foo': {'lorem': 'ipsum'},
        }
        config = Config(config_dict)

        self.assertFalse(config.is_empty())

        foo_config = config.get('foo')

        self.assertFalse(foo_config.is_empty())

        self.assertEqual(foo_config.get_value('lorem'), 'ipsum')
        self.assertEqual(foo_config.get_value('lorem', 'dolor'), 'ipsum')
        self.assertEqual(foo_config.get_value('bar', 'dolor'), 'dolor')

    def test_config_point_syntax(self):
        config_dict = {
            'tool': {'autohooks': {'plugins': {'bar': {'lorem': 'ipsum'}}}}
        }

        config = Config(config_dict)

        self.assertFalse(config.is_empty())

        bar_config = config.get('tool', 'autohooks', 'plugins', 'bar')
        self.assertFalse(bar_config.is_empty())
        self.assertEqual(bar_config.get_value('lorem'), 'ipsum')


if __name__ == '__main__':
    unittest.main()
