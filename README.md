![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)

# Autohooks

Library for managing and writing [git hooks](https://git-scm.com/docs/githooks)
in Python

## Why

Several outstanding libraries for managing and executing git hooks already
exist. To name few: [husky](https://github.com/typicode/husky),
[lint-staged](https://github.com/okonet/lint-staged),
[precise-commits](https://github.com/nrwl/precise-commits) or
[pre-commit](https://github.com/pre-commit/pre-commit).

But either they need another interpreter besides python like husky or they are
too ambiguous like pre-commit. pre-commit is written in python but has support
hooks written in all kind of languages. Also it maintains the dependencies by
itself and doesn't install in the current environment.

## Solution

Authooks is a pure python library that installs a minimal
[executable git hook](https://github.com/bjoernricks/autohooks/blob/master/autohooks/precommit/template).
If autohooks isn't installed in your current python path the hooks aren't
executed. So autohooks is always opt-in by installing the package into your
current development environment. It would be even possible to run different
versions of autohooks by switching the environment.
