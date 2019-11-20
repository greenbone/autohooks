![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)

# Autohooks <!-- omit in toc -->

[![PyPI release](https://img.shields.io/pypi/v/autohooks.svg)](https://pypi.org/project/autohooks/)

Library for managing and writing [git hooks](https://git-scm.com/docs/githooks)
in Python

- [Why?](#why)
- [Solution](#solution)
- [Modes](#modes)
  - [Pythonpath Mode](#pythonpath-mode)
  - [Pipenv Mode](#pipenv-mode)
  - [Poetry Mode](#poetry-mode)
- [Installation](#installation)
  - [Choose autohooks Mode](#choose-autohooks-mode)
  - [Install autohooks Python Package](#install-autohooks-python-package)
  - [Configure Plugins to be run](#configure-plugins-to-be-run)
  - [Activating the Git Hooks](#activating-the-git-hooks)
- [Plugins](#plugins)
- [How-to write a Plugin](#how-to-write-a-plugin)
  - [Linting Plugin](#linting-plugin)
  - [Formatting Plugin](#formatting-plugin)
- [Maintainer](#maintainer)
- [Contributing](#contributing)
- [License](#license)

## Why?

Several outstanding libraries for managing and executing git hooks already
exist. To name few: [husky](https://github.com/typicode/husky),
[lint-staged](https://github.com/okonet/lint-staged),
[precise-commits](https://github.com/nrwl/precise-commits) or
[pre-commit](https://github.com/pre-commit/pre-commit).

But either they need another interpreter besides python (like husky) or they are
too ambiguous (like pre-commit). pre-commit is written in python but has support
hooks written in all kind of languages. Also it maintains the dependencies by
itself and doesn't install in the current environment.

## Solution

Autohooks is a pure python library that installs a minimal
[executable git hook](https://github.com/greenbone/autohooks/blob/master/autohooks/precommit/template).
It allows you to decide how to maintain your hook dependencies by supporting
different modes.

## Modes

Currently three modes for using autohooks are supported:

* `pythonpath`
* `pipenv`
* `poetry`

The modes handle how autohooks, the plugins and their dependencies are loaded
during git hook execution.

If no mode is specified in the [`pyproject.toml` config file](#configure-mode-and-plugins-to-be-run)
and no mode is set during [activation](#activating-the-git-hooks), autohooks
will use the [pythonpath mode](#pythonpath-mode) by default.

### Pythonpath Mode

In the `pythonpath` mode the user has to install autohooks, the desired
plugins and their dependencies into the [PYTHONPATH](https://docs.python.org/3/library/sys.html#sys.path)
manually.

This can be achieved by running `pip install --user autohooks ...` to put them
into the installation directory of the [current user](https://docs.python.org/3/library/site.html#site.USER_SITE)
or with `pip install authooks ...` for a system wide installation.

Alternatively a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments)
could be used, which separates the installation from your global and user wide
Python packages.

It would also be possible to use [pipenv] for the management of the virtual
environment but the activation of the environment has to be done manually.

Therefore it would be even possible to run different versions of autohooks by
using the `pythonpath` mode and switching a virtual environment.

### Pipenv Mode

In the `pipenv` mode [pipenv] is used to run autohooks in a dedicated virtual
environment. Pipenv uses a lockfile to install exact versions. Therefore the
installation is deterministic and reliable between different developer setups.
In contrast to the `pythonpath` mode the activation of the virtual environment
provided by [pipenv] is done automatically in the background.

Using the `pipenv` mode is highly recommended.

### Poetry Mode

Like the [pipenv mode](#pipenv-mode) it is possible to run autohooks in a
dedicated environment controlled by [poetry]. By using the `poetry` mode the
virtual environment will be activated automatically in the background when
executing the autohooks based git commit hook.

## Installation

For the installation of autohooks three steps are necessary:

1. Choose autohooks mode
2. Install autohooks package into your current environment
3. Configure plugins to be run
4. Activate [git hooks](https://git-scm.com/docs/githooks)

### Choose autohooks Mode

Autohooks uses the *pyproject.toml* file specified in
[PEP518](https://www.python.org/dev/peps/pep-0518/) for its configuration.
Adding a *[tool.autohooks]* section allows to specify the desired [autohooks mode](#modes)
and to set python modules to be run as [autohooks plugins](#plugins).

The mode can be set by adding a `mode =` line to the *pyproject.toml* file.
Current possible options are `"pythonpath"`, `"pipenv"` and `"poetry"`. See
[autohooks mode](#modes) for more details. If the mode setting is missing it
falls back to `pythonpath` mode.

Example *pyproject.toml*:

```toml
[build-system]
requires = ["setuptools", "wheel"]

[tool.autohooks]
mode = "pipenv"
```

### Install autohooks Python Package

For installing the autohooks python package, using [pipenv] is highly
recommended.

To install autohooks as a development dependency run

```sh
pipenv install --dev autohooks
```

or add

```toml
autohooks = "*"
```

to the `[dev-packages]` section of your `Pipfile`.

Alternatively autohooks can be installed directly from GitHub by running

```sh
pipenv install --dev git+https://github.com/greenbone/autohooks#egg=autohooks
```

or adding

```toml
autohooks = {git = "https://github.com/greenbone/autohooks"}
```

to the `[dev-packages]` section of your `Pipfile`.

### Configure Plugins to be run

To actually run an action on git hooks, [autohooks plugins](#plugins) have to be
installed and configured. To install e.g. python linting via pylint run

```bash
pipenv install --dev autohooks-plugin-pylint
```

Afterwards the pylint plugin can be configured to run as a pre-commit git hook
by adding the autohooks-plugins-pylint python module name to the `pre-commit`
setting at the `[tool.autohooks]` section in the *pyproject.toml* file.

Example *pyproject.toml*:

```toml
[build-system]
requires = ["setuptools", "wheel"]

[tool.autohooks]
mode = "pipenv"
pre-commit = ["autohooks.plugins.pylint"]
```

### Activating the Git Hooks

If autohooks is installed from git or a source tarball, the git hooks should be
activated automatically. The activation can be verified by running e.g.
`autohooks check`.

Installing autohooks from a [wheel](https://www.python.org/dev/peps/pep-0427/)
package will **NOT** activate the git commit hooks automatically.

To manually activate the git hooks you can run

```bash
pipenv run autohooks activate
```

Calling `activate` also allows for overriding the [mode](#modes) defined in the
*pyproject.toml* settings for testing purposes. E.g.

```bash
pipenv run autohooks activate --mode pipenv
```

Please keep in mind that autohooks will always issue a warning if the mode used
in the git hooks is different from the configured mode in the *pyproject.toml*
file.

## Plugins

* Python code formatting via [black](https://github.com/greenbone/autohooks-plugin-black)

* Python code formatting via [autopep8](https://github.com/LeoIV/autohooks-plugin-autopep8)

* Python code linting via [pylint](https://github.com/greenbone/autohooks-plugin-pylint)

* Python import sorting via [isort](https://github.com/greenbone/autohooks-plugin-isort)

## How-to write a Plugin

Plugins need to be available in the
[Python import path](https://docs.python.org/3/reference/import.html). The
easiest way to achieve this, is to upload a plugin to [PyPI](https://pypi.org/)
and install it via [pip] or [pipenv].

Alternatively, a plugin can also be put into a *.autohooks* directory at the root
directory of the git repository where the hooks should be executed.

An autohooks plugin is a Python module which provides a **precommit** function.
The function must accept arbitrary keywords because the keywords are likely to
change in future. Therefore using **\*\*kwargs** is highly recommended.
Currently only a *config* keyword argument is passed to the precommit function.
E.g.

```python3
def precommit(**kwargs):
    config = kwargs.get('config')
```

The config can be used to receive settings from the *pyproject.toml* file. E.g.

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

With autohooks it is possible to write all kinds of plugins. Most common are
plugins for linting and formatting.

### Linting Plugin

Usually the standard call sequence for a linting plugin is

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
    return config.get_value('include', DEFAULT_INCUDE)


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
                fail('Could not validate {}'.format(str(file)))
                failed = True
            else:
                ok('Validated {}'.format(str(file)))

        return 1 if failed else 0
```

### Formatting Plugin

Usually the standard call sequence for a formatting plugin is

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
    return config.get_value('include', DEFAULT_INCUDE)


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
            ok('Formatted {}'.format(str(file)))

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

Copyright (C) 2019 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).

[pip]: https://pip.pypa.io/
[pipenv]: https://pipenv.readthedocs.io/
[poetry]: https://poetry.eustace.io/
