![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)
# Autohooks <!-- omit in toc -->

[![PyPI release](https://img.shields.io/pypi/v/autohooks.svg)](https://pypi.org/project/autohooks/)
[![Build and test Python package](https://github.com/greenbone/autohooks/actions/workflows/ci-python.yml/badge.svg)](https://github.com/greenbone/autohooks/actions/workflows/ci-python.yml)
[![codecov](https://codecov.io/gh/greenbone/autohooks/branch/main/graph/badge.svg?token=9IX7ucaFwj)](https://codecov.io/gh/greenbone/autohooks)

Library for managing and writing [git hooks](https://git-scm.com/docs/githooks)
in Python.

Looking for automatic formatting or linting, e.g., with [black] and [pylint],
while creating a git commit using a pure Python implementation?
Welcome to **autohooks**!

- [Why?](#why)
- [Solution](#solution)
- [Requirements](#requirements)
- [Modes](#modes)
  - [Pythonpath Mode](#pythonpath-mode)
  - [Poetry Mode](#poetry-mode)
  - [Pipenv Mode](#pipenv-mode)
- [Installing autohooks](#installing-autohooks)
  - [1. Choosing an autohooks Mode](#1-choosing-an-autohooks-mode)
  - [2. Installing the autohooks Python Package into the Current Environment](#2-installing-the-autohooks-python-package-into-the-current-environment)
  - [3. Configuring Plugins to Be Run](#3-configuring-plugins-to-be-run)
  - [4. Activating the Git Hooks](#4-activating-the-git-hooks)
- [Plugins](#plugins)
- [Howto: Writing a Plugin](#howto-writing-a-plugin)
  - [Linting Plugin](#linting-plugin)
  - [Formatting Plugin](#formatting-plugin)
- [Maintainer](#maintainer)
- [Contributing](#contributing)
- [License](#license)

## Why?

Several outstanding libraries for managing and executing git hooks exist already.
To name a few: [husky](https://github.com/typicode/husky),
[lint-staged](https://github.com/okonet/lint-staged),
[precise-commits](https://github.com/nrwl/precise-commits) or
[pre-commit](https://github.com/pre-commit/pre-commit).

However, they either need another interpreter besides python (like husky) or are
too ambiguous (like pre-commit). pre-commit is written in python but has support
hooks written in all kind of languages. Additionally, it maintains the dependencies by
itself and does not install them in the current environment.

## Solution

autohooks is a pure python library that installs a minimal
[executable git hook](https://github.com/greenbone/autohooks/blob/main/autohooks/precommit/template).
It allows the decision of how to maintain the hook dependencies
by supporting different modes.

![Autohooks](https://raw.githubusercontent.com/greenbone/autohooks/main/autohooks.gif)

## Requirements

Python 3.7+ is required for autohooks.

## Modes

Currently three modes for using autohooks are supported:

* `pythonpath`
* `poetry`
* `pipenv`

These modes handle how autohooks, the plugins and their dependencies are loaded
during git hook execution.

If no mode is specified in the [`pyproject.toml` config file](#configure-mode-and-plugins-to-be-run)
and no mode is set during [activation](#activating-the-git-hooks), autohooks
will use the [pythonpath mode](#pythonpath-mode) by default.

`poetry` or `pipenv` modes leverage the `/usr/bin/env` command using the
`--split-string` (`-S`) option. If `autohooks` detects that it is
running on an OS where `/usr/bin/env` is yet to support _split_strings_
(notably ubuntu < 19.x), `autohooks` will automatically change to an
internally chosen `poetry_multiline`/`pipenv_mutliline` mode. The
'multiline' modes *should not* be user-configured options; setting your
project to use `poetry` or `pipenv`allows team members the greatest
latitude to use an OS of their choice yet leverage the sane
`/usr/bin/env --split-string` if possible. Though `poetry_multiline`
would generally work for all, it is very confusing sorcery.
([Multiline shebang explained](https://rosettacode.org/wiki/Multiline_shebang#Python))

### Pythonpath Mode

In the `pythonpath` mode, the user has to install autohooks, the desired
plugins and their dependencies into the [PYTHONPATH](https://docs.python.org/3/library/sys.html#sys.path)
manually.

This can be achieved by running `python3 -m pip install --user autohooks ...` to put them
into the installation directory of the [current user](https://docs.python.org/3/library/site.html#site.USER_SITE)
or with `python3 -m pip install autohooks ...` for a system wide installation.

Alternatively, a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments)
could be used separating the installation from the global and user wide
Python packages.

It is also possible to use [pipenv] for managing the virtual
environment but activating the environment has to be done manually.

Therefore it is even possible to run different versions of autohooks by
using the `pythonpath` mode and switching to a virtual environment.

### Poetry Mode

Like with the [pipenv mode](#pipenv-mode), it is possible to run autohooks in a
dedicated environment controlled by [poetry]. By using the `poetry` mode the
virtual environment will be activated automatically in the background when
executing the autohooks based git commit hook.

Using the `poetry` mode is highly recommended.

### Pipenv Mode

In the `pipenv` mode [pipenv] is used to run autohooks in a dedicated virtual
environment. Pipenv uses a lock file to install exact versions. Therefore the
installation is deterministic and reliable between different developer setups.
In contrast to the `pythonpath` mode the activation of the virtual environment
provided by [pipenv] is done automatically in the background.

## Installing autohooks

Four steps are necessary for installing autohooks:

1. Choosing an autohooks mode
2. Installing the autohooks python package into the current environment
3. Configuring plugins to be run
4. Activating the [git hooks](https://git-scm.com/docs/githooks)

### 1. Choosing an autohooks Mode

For its configuration, autohooks uses the *pyproject.toml* file specified in
[PEP518](https://www.python.org/dev/peps/pep-0518/).
Adding a *[tool.autohooks]* section allows to specify the desired [autohooks mode](#modes)
and to set python modules to be run as [autohooks plugins](#plugins).

The mode can be set by adding a `mode =` line to the *pyproject.toml* file.
Current possible options are `"pythonpath"`, `"pipenv"` and `"poetry"` (see
[autohooks mode](#modes)). If the mode setting is missing, the `pythonpath` mode is used.

Example *pyproject.toml*:

```toml
[tool.autohooks]
mode = "pipenv"
```

### 2. Installing the autohooks Python Package into the Current Environment

Using [poetry] is highly recommended for installing the autohooks python package.

To install autohooks as a development dependency run

```sh
poetry add --dev autohooks
```

Alternatively, autohooks can be installed directly from GitHub by running

```sh
poetry add --dev git+https://github.com/greenbone/autohooks
```

### 3. Configuring Plugins to Be Run

To actually run an action on git hooks, [autohooks plugins](#plugins) have to be
installed and configured, e.g., to install python linting via pylint run

```bash
poetry add --dev autohooks-plugin-pylint
```

Afterwards, the pylint plugin can be configured to run as a pre-commit git hook
by adding the autohooks-plugins-pylint python module name to the `pre-commit`
setting in the `[tool.autohooks]` section in the *pyproject.toml* file.

Example *pyproject.toml*:

```toml
[tool.autohooks]
mode = "pipenv"
pre-commit = ["autohooks.plugins.pylint"]
```

### 4. Activating the Git Hooks

Because installing and activating git hooks automatically isn't reliable (with
using source distributions and different versions of pip) and even impossible
(with using [wheels](https://www.python.org/dev/peps/pep-0427/)) the hooks need
to be activated manually once in each installation.

To activate the git hooks run

```bash
poetry run autohooks activate
```

Calling `activate` also allows for overriding the [mode](#modes) defined in the
*pyproject.toml* settings for testing purposes.

Example:


```bash
autohooks activate --mode pipenv
```

Please keep in mind that autohooks will always issue a warning if the mode used
in the git hooks is different from the configured mode in the *pyproject.toml*
file.

The activation can always be verified by running `autohooks check`.

## Plugins

* Python code formatting via [black](https://github.com/greenbone/autohooks-plugin-black)

* Python code formatting via [autopep8](https://github.com/LeoIV/autohooks-plugin-autopep8)

* Python code linting via [pylint](https://github.com/greenbone/autohooks-plugin-pylint)

* Python code linting via [flake8](https://github.com/greenbone/autohooks-plugin-flake8)

* Python import sorting via [isort](https://github.com/greenbone/autohooks-plugin-isort)

* Running tests via [pytest](https://github.com/greenbone/autohooks-plugin-pytest/)

## Howto: Writing a Plugin

Plugins need to be available in the
[Python import path](https://docs.python.org/3/reference/import.html). The
easiest way to achieve this is uploading a plugin to [PyPI](https://pypi.org/)
and installing it via [pip] or [poetry].

Alternatively, a plugin can also be put into a *.autohooks* directory in the root
directory of the git repository where the hooks should be executed.

An autohooks plugin is a Python module which provides a **precommit** function.
The function must accept arbitrary keywords because the keywords are likely to
change in future. Therefore using **\*\*kwargs** is highly recommended.
Currently *config* and *report_progress* keyword arguments are passed to the
precommit function.

Example:

```python3
def precommit(config=None, report_progress=None, **kwargs):
```

The config can be used to receive settings from the *pyproject.toml* file, e.g.,

```toml
[tool.autohooks.plugins.foo]
bar = 2
```

can be received with

```python3
def precommit(**kwargs):
    config = kwargs.get('config')
    default_value = 1
    setting = config
      .get('tool', 'autohooks', 'plugins', 'foo')
      .get_value('bar', default_value)
    return 0
```

The report_progress can be used since autohooks 22.8.0 to display a progress bar
when running a plugin.

```python3
def precommit(report_progress, **kwargs):
    report_progress.init(len(files))

    for file in files:
      check_file(file)
      report_progress.update()

    return 0
```
With autohooks it is possible to write all kinds of plugins. Most common are
plugins for linting and formatting.

### Linting Plugin

Usually the standard call sequence for a linting plugin is the following:

1. get list of staged files
2. filter list of files for a specific file type
3. stash unrelated changes
4. apply checks on filtered list of files by calling some external tool
5. raise exception if something did go wrong
6. return 1 if check was not successful
6. stage changes made by the tool
7. unstash unrelated changes
8. return 0

Example plugin:

```python3
import subprocess

from autohooks.api import ok, fail
from autohooks.api.git import get_staged_status, stash_unstaged_changes
from autohooks.api.path import match

DEFAULT_INCLUDE = ('*.ext')


def get_include(config)
    if not config:
        return DEFAULT_INCLUDE

    config = config.get('tool', 'autohooks', 'plugins', 'foo')
    return config.get_value('include', DEFAULT_INCLUDE)


def precommit(**kwargs):
    config = kwargs.get('config')
    include = get_include(config)

    files = [f for f in get_staged_status() if match(f.path, include)]

    if not files:
      # not files to lint
      return 0

    with stash_unstaged_changes(files):
        const failed = False
        for file in files:
            status = subprocess.call(['foolinter', str(file)])
            if status:
                fail('Could not validate {str(file)}')
                failed = True
            else:
                ok('Validated {str(file)}')

        return 1 if failed else 0
```

### Formatting Plugin

Usually the standard call sequence for a formatting plugin is the following:

1. get list of staged files
2. filter list of files for a specific file type
3. stash unrelated changes
4. apply formatting on filtered list of files by calling some external tool
5. raise exception if something did go wrong
6. stage changes made by the tool
7. unstash unrelated changes
8. return 0

Example plugin:

```python3
import subprocess

from autohooks.api import ok, error
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match

DEFAULT_INCLUDE = ('*.ext')


def get_include(config)
    if not config:
        return DEFAULT_INCLUDE

    config = config.get('tool', 'autohooks', 'plugins', 'bar')
    return config.get_value('include', DEFAULT_INCLUDE)


def precommit(**kwargs):
    config = kwargs.get('config')
    include = get_include(config)

    files = [f for f in get_staged_status() if match(f.path, include)]

    if not files:
      # not files to format
      return 0

    with stash_unstaged_changes(files):
        for file in files:
            # run formatter and raise exception if it fails
            subprocess.run(['barformatter', str(file)], check=True)
            ok('Formatted {str(file)}')

        return 0
```

## Maintainer

This project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).

## Contributing

Your contributions are highly appreciated. Please
[create a pull request](https://github.com/greenbone/autohooks/pulls)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at GitHub](https://github.com/greenbone/autohooks/issues)
first.

## License

Copyright (C) 2019 - 2022 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).

[black]: https://black.readthedocs.io/en/stable/
[pip]: https://pip.pypa.io/en/stable/
[pipenv]: https://pipenv.readthedocs.io/en/latest/
[poetry]: https://python-poetry.org/
[pylint]: https://pylint.readthedocs.io/en/latest/
