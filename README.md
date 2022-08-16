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
- [Plugins](#plugins)
- [Installing autohooks](#installing-autohooks)
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

## Plugins

* Python code formatting via [black](https://github.com/greenbone/autohooks-plugin-black)

* Python code formatting via [autopep8](https://github.com/LeoIV/autohooks-plugin-autopep8)

* Python code linting via [pylint](https://github.com/greenbone/autohooks-plugin-pylint)

* Python code linting via [flake8](https://github.com/greenbone/autohooks-plugin-flake8)

* Python import sorting via [isort](https://github.com/greenbone/autohooks-plugin-isort)

* Running tests via [pytest](https://github.com/greenbone/autohooks-plugin-pytest/)

## Installing autohooks

Quick installation of [pylint] and [black] plugins using [poetry]:

```shell
poetry add --dev autohooks autohooks-plugin-black autohooks-plugin-pylint
poetry run autohooks activate --mode poetry
poetry run autohooks plugins add autohooks.plugins.black autohooks.plugins.pylint
```

The output of `autohooks activate` should be similar to
```
 ✓ autohooks pre-commit hook installed at /autohooks-test/.git/hooks/pre-commit using poetry mode.
```

Autohooks has an extensible plugin model. Each plugin provides different
functionality which often requires to install additional dependencies.

For managing these dependencies currently three modes are supported by
autohooks:

* `pythonpath` for dependency management via [pip]
* `poetry` for dependency management via [poetry] (recommended)
* `pipenv` for dependency management via [pipenv]

These modes handle how autohooks, the plugins and their dependencies are loaded
during git hook execution.

If no mode is specified in the [`pyproject.toml` config file](#configure-mode-and-plugins-to-be-run)
and no mode is set during [activation](#activating-the-git-hooks), autohooks
will use the [pythonpath mode](#pythonpath-mode) by default.

For more details on using [pip], [poetry] or [pipenv] in conjunction with these
modes see the [documentation](https://greenbone.github.io/autohooks).

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
