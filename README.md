![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)

# Autohooks

[![PyPI release](https://img.shields.io/pypi/v/autohooks.svg)](https://pypi.org/project/autohooks/)

Library for managing and writing [git hooks](https://git-scm.com/docs/githooks)
in Python

## Why

Several outstanding libraries for managing and executing git hooks already
exist. To name few: [husky](https://github.com/typicode/husky),
[lint-staged](https://github.com/okonet/lint-staged),
[precise-commits](https://github.com/nrwl/precise-commits) or
[pre-commit](https://github.com/pre-commit/pre-commit).

But either they need another interpreter besides python (like husky) or they are
too ambiguous like (pre-commit). pre-commit is written in python but has support
hooks written in all kind of languages. Also it maintains the dependencies by
itself and doesn't install in the current environment.

## Solution

Autohooks is a pure python library that installs a minimal
[executable git hook](https://github.com/bjoernricks/autohooks/blob/master/autohooks/precommit/template).
If autohooks isn't installed in your current python path the hooks aren't
executed. So autohooks is always opt-in by installing the package into your
current development environment. It would be even possible to run different
versions of autohooks by switching the environment.

## Installation

For the installation of autohooks three steps are necessary:

1. Install the autohooks package into your current environment
2. Activate the [git hooks](https://git-scm.com/docs/githooks)
3. Configure the plugins to be run

### Install autohooks python package

For installing the autohooks python package, using
[pipenv](https://pipenv.readthedocs.io/en/latest/) is highly recommended.

To install autohooks as a development dependency run

```sh
pipenv install --dev autohooks
```

Alternatively autohooks can be installed directly from GitHub

```sh
pipenv install --dev -e git+https://github.com/bjoernricks/autohooks#egg=autohooks
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

To actually run an action on git hooks, autohooks plugins have to be configured.
Autohooks uses the *pyproject.toml* file specified in [PEP518](https://www.python.org/dev/peps/pep-0518/)
for its configuration. Adding a *[tool.autohooks]* section allows to set python
modules to be run on a specific git hook.

Example *pyproject.toml*:
```toml
[build-system]
requires = ["setuptools", "wheel"]

[tool.autohooks]
pre-commit = ["autohooks.plugins.black"]
```

## Plugins

* Python code formatting via [black](https://github.com/bjoernricks/autohooks-plugin-black)

* Python code linting via [pylint](https://github.com/bjoernricks/autohooks-plugin-pylint)

## Maintainer

This project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).

## Contributing

Your contributions are highly appreciated. Please
[create a pull request](https://github.com/bjoernricks/autohooks/pulls)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at GitHub](https://github.com/bjoernricks/autohooks/issues)
first.

## License

Copyright (C) 2019 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).
