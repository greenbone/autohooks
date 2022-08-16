
# Autohooks

```{image} _static/greenbone.png
:alt: Greenbone Logo
:width: 300px
:target: ""
:class: greenbone-logo
````

Library for managing and writing [git hooks](https://git-scm.com/docs/githooks)
in Python.

Looking for automatic formatting or linting, e.g., with [black] and [pylint],
while creating a git commit using a pure Python implementation?
Welcome to **autohooks**!

## Why?

Several outstanding libraries for managing and executing git hooks exist already.
To name a few: [husky](https://github.com/typicode/husky),
[lint-staged](https://github.com/okonet/lint-staged),
[precise-commits](https://github.com/nrwl/precise-commits) or
[pre-commit](https://github.com/pre-commit/pre-commit).

However, they either need another interpreter besides python (like husky) or are
too ambiguous (like pre-commit). pre-commit is written in Python but has support
hooks written in all kind of languages. Additionally, it maintains the dependencies by
itself and does not install them in the current environment.

## Solution

autohooks is a pure Python library that installs a minimal
[executable git hook](https://github.com/greenbone/autohooks/blob/main/autohooks/precommit/template).
It allows the decision of how to maintain the hook dependencies
by supporting different [modes](./modes.md).

![Autohooks](https://raw.githubusercontent.com/greenbone/autohooks/main/autohooks.gif)

## Requirements

Python 3.7+ is required for autohooks. It depends on [tomlkit](https://github.com/sdispater/tomlkit/),
[pontos](https://github.com/greenbone/pontos) and [rich](https://github.com/Textualize/rich/).

```{toctree}
:hidden:

quickstart
installation
configuration
modes
plugins
```

```{toctree}
:caption: Development
:hidden:

create
api
```

[black]: https://black.readthedocs.io/en/stable/
[pylint]: https://pylint.readthedocs.io/en/latest/
