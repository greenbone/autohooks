![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)

# Autohooks

[![PyPI release](https://img.shields.io/pypi/v/autohooks.svg)](https://pypi.org/project/autohooks/)

Library for managing and writing [git hooks](https://git-scm.com/docs/githooks)
in Python

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
If autohooks isn't installed in your current python path the hooks aren't
executed. So autohooks is always opt-in by installing the package into your
current development environment. It would be even possible to run different
versions of autohooks by switching the environment.

Autohooks doesn't interfere with your work. If autohooks can't be run or fails
executing a plugin, an error is shown only and the git hook will proceed.

## Installation

For the installation of autohooks three steps are necessary:

1. Install the autohooks package into your current environment
2. Activate the [git hooks](https://git-scm.com/docs/githooks)
3. Configure the plugins to be run

### Install autohooks python package

For installing the autohooks python package, using
[pipenv](https://pipenv.readthedocs.io/) is highly recommended.

To install autohooks as a development dependency run

```sh
pipenv install --dev autohooks
```

Alternatively autohooks can be installed directly from GitHub

```sh
pipenv install --dev -e git+https://github.com/greenbone/autohooks#egg=autohooks
```

### Activating the git hooks

If autohooks is installed from git or a source tarball, the git hooks should be
activated automatically. The activation can be verified by running e.g.
`autohooks check`.

Installing autohooks from a [wheel](https://www.python.org/dev/peps/pep-0427/)
package will **NOT** activate the git commit hooks.

To manually activate the git hooks you can run

```sh
pipenv run autohooks activate
```

### Configure plugins to be run

To actually run an action on git hooks, [autohooks plugins](#plugins) have to be
installed and configured. To install e.g. python linting via pylint run

```
pipenv install --dev autohooks-plugin-pylint
```

Autohooks uses the *pyproject.toml* file specified in
[PEP518](https://www.python.org/dev/peps/pep-0518/) for its configuration.
Adding a *[tool.autohooks]* section allows to set python modules to be run on a
specific git hook.

Example *pyproject.toml*:

```toml
[build-system]
requires = ["setuptools", "wheel"]

[tool.autohooks]
pre-commit = ["autohooks.plugins.black"]
```

## Proposed Workflow

Using [pipenv](https://pipenv.readthedocs.io/) allows to install all
dependencies and tools with a specific version into a virtual, easily removable
Python environment. Therefore it's best to maintain **autohooks** also via
pipenv. Because it is not required to build or run your software, it should be
[installed as a development dependency](#install-autohooks-python-package).
Installing and [activating](#activating-the-git-hooks) autohooks doesn't
actually run any check or formatting by itself. Therefore, it is required to
[choose and install a plugin](#configure-plugins-to-be-run).

If all these tasks have been resolved, the developers are able to install
and activate autohooks with only one single command from your project's git
repository:

```sh
pipenv install --dev
```

Because virtual environments are used for all dependencies including
autohooks, the linting, formatting, etc. can only by done when running
`git commit` within the virtual environment.

```sh
$ cd myproject
$ pipenv install --dev
$ pipenv shell
(myproject)$ git commit
```

The advantage of this process is, if the user is not running `git commit` within
the active virtual environment, autohooks and its plugins are not executed.

```sh
$ cd myproject
$ git commit
```

This allows the user to choose whether to execute the hooks by activating the
virtual environment or to ignore them by deactivating it.

## Plugins

* Python code formatting via [black](https://github.com/greenbone/autohooks-plugin-black)

* Python code linting via [pylint](https://github.com/greenbone/autohooks-plugin-pylint)

## How-to write a Plugin

Plugins need to be available in the
[Python import path](https://docs.python.org/3/reference/import.html). The
easiest way to achieve this, is to upload a plugin to [PyPI](https://pypi.org/)
and install it via [pip]() or [pipenv](http://pipenv.readthedocs.io/).

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

### Linting plugin

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

### Formatting plugin

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
