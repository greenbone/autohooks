# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org).

For detailed code changes, please visit
https://github.com/greenbone/autohooks/commits/main
or get the entire source code repository and view log history:

```sh
$ git clone https://github.com/greenbone/autohooks.git
$ cd autohooks && git log
```

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed

[Unreleased]: https://github.com/greenbone/autohooks/compare/v21.7.0...HEAD


## [21.7.0] - 2021-07-19
### Changed
* Using `Path.cwd()` instead of `os.environ['PWD']`, to make autohooks more reliable for windows. [#165](https://github.com/greenbone/autohooks/pull/165)

[21.7.0]: https://github.com/greenbone/autohooks/compare/v21.6.0...v21.7.0

## [21.6.0] - 2021-06-13
### Fixed
* Fix getting a value from the config with tomlkit >= 0.7.1 [#132](https://github.com/greenbone/autohooks/pull/132)

[21.6.0]: https://github.com/greenbone/autohooks/compare/v21.3.0...v21.6.0

## [21.3.0] - 2021-03-29
### Added
* CI tests Python 3.9 now. [#97](https://github.com/greenbone/autohooks/pull/97)

### Deprecated
* Dropped Python 3.5 and Python 3.6 support. Python 3.7+ is required now. [#97](https://github.com/greenbone/autohooks/pull/97)

### Fixed
* Fix split-string (`-S`) to support all operating systems. [#89](https://github.com/greenbone/autohooks/pull/89)

[21.3.0]: https://github.com/greenbone/autohooks/compare/v2.2.0...v21.3.0

## [2.2.0] - 2020-08-28

### Added

* Major style changes: Moved from textual status at the end of a line to an symbolic status in front of the text. [#66](https://github.com/greenbone/autohooks/pull/66)

### Removed

* Use version handling via [pontos](https://github.com/greenbone/pontos) and
  remove all version handling code again [#57](https://github.com/greenbone/autohooks/pull/57)

[Unrelased]: https://github.com/greenbone/autohooks/compare/v2.1.0...main

## [2.1.0] - 2020-04-09

### Added

* Added tools for version handling in autohooks [#51](https://github.com/greenbone/autohooks/pull/51)
* Added static `get_width` method to Terminal class [#53](https://github.com/greenbone/autohooks/pull/53)

### Changed

* Reworked `Terminal` class from `terminal.py` [#45](https://github.com/greenbone/autohooks/pull/45)
* Replaced pipenv with poetry for dependency management. `poetry install` works a
  bit different than `pipenv install`. It installs dev packages and also autohooks
  in editable mode by default. [#51](https://github.com/greenbone/autohooks/pull/51)
* Activation of the git hooks must be done manually with `autohooks activate`
  always. Using source distributions and a setuptools extension to activate the
  hooks isn't reliable at all [#52](https://github.com/greenbone/autohooks/pull/52)
* Recommend the `poetry` mode instead of the `pipenv` mode. poetry is more
  reliable than pipenv [#55](https://github.com/greenbone/autohooks/pull/55)

### Fixed

* Windows Support, by exchanging the unmaintained `blessing` module through
  [`colorful`](https://github.com/timofurrer/colorful)
  [#45](https://github.com/greenbone/autohooks/pull/45)
* Fixed running `autohooks check` if no `.git/hooks/pre-commit` file exists
  [#49](https://github.com/greenbone/autohooks/pull/49)

### Removed

* Removed code relying on setuptools and switched to a full poetry build
  process [#54](https://github.com/greenbone/autohooks/pull/54)

[2.1.0]: https://github.com/greenbone/autohooks/compare/v2.0.0...v2.1.0

## [2.0.0] - 2019-11-20

### Added

* Introduction of autohooks modes. Modes configure how to handle loading
  autohooks, plugins and dependencies when running the git hook. The
  `pythonpath` mode requires to put the necessary python packages into the
  **PYTHONPATH** manually. The `pipenv` mode uses pipenv to handle the
  dependencies. Using the `pipenv` mode is recommended.
  [#24](https://github.com/greenbone/autohooks/pull/24)
* Add `poetry` mode to run autohooks via [poetry](https://poetry.eustace.io/)
  [#29](https://github.com/greenbone/autohooks/pull/29)
* Added type hints/annotations to all methods [#32](https://github.com/greenbone/autohooks/pull/32)
* Added version meta information to installed pre commit hook
  [#30](https://github.com/greenbone/autohooks/pull/30)
* Extended autohooks check cli to evaluate current hook version and used mode
  [#30](https://github.com/greenbone/autohooks/pull/30)
* Enhanced autohooks activate cli to show additional information if a autohooks
  git hook is already installed
  [#30](https://github.com/greenbone/autohooks/pull/30)
* Added plugin API for additional info status output
  [#39](https://github.com/greenbone/autohooks/pull/39)
* Added plugin API for additional message printing
  [#39](https://github.com/greenbone/autohooks/pull/39)

### Changed

* The installed git hook will fail now if autohooks can't be loaded. Before the
  git hook raised only a warning and was ignored. This a major change compared
  to the previous versions. To update existing installations it requires
  overriding the installed git hook by running `autohooks activate --force`.
  [#24](https://github.com/greenbone/autohooks/pull/24)
* The installed git hook will fail now if a autohooks plugin can't be executed
  e.g. if the import fails. Before these errors were ignored.
  [#28](https://github.com/greenbone/autohooks/pull/28)
* The version of the installed git hook is checked during its execution
  [#30](https://github.com/greenbone/autohooks/pull/30)
* A warning is raised during git hook execution if the current mode is different
  to the configured mode [#30](https://github.com/greenbone/autohooks/pull/30)
* Improved output formatting [#39](https://github.com/greenbone/autohooks/pull/39)

[2.0.0]: https://github.com/greenbone/autohooks/compare/v1.1.0...v2.0.0

## [1.1.0] - 2019-03-27

### Added

* Updated README.md about proposed workflow
  [#4](https://github.com/greenbone/autohooks/pull/4)
* Allow to load plugins from a *.autohooks* directory in the git repository root
  directory [#6](https://github.com/greenbone/autohooks/pull/6)
* Added a plugin API for getting a git diff
  [#8](https://github.com/greenbone/autohooks/pull/8)
* Added a plugin API for matching files against a list of patterns
  [#9](https://github.com/greenbone/autohooks/pull/9)
* Added plugin API for status output: ok, warning, fail and error
  [#14](https://github.com/greenbone/autohooks/pull/14)

### Changed

* Changed git repository location to https://github.com/greenbone/autohooks
* Extend config file handling [#7](https://github.com/greenbone/autohooks/pull/7)
* **precommit** plugin functions should accept `**kwargs` now
  [#7](https://github.com/greenbone/autohooks/pull/7). This will be mandatory
  with a 2.0 release.
* A Config class instance is passed as config keyword argument to the
  **precommit** plugin function. It can be used to receive plugin specific
  settings [#7](https://github.com/greenbone/autohooks/pull/7)
* Improved check cli to verify settings and specified plugins
  [#12](https://github.com/greenbone/autohooks/pull/12)
* Improved and colorized terminal output [#14](https://github.com/greenbone/autohooks/pull/14)
* Show a warning if changes created by formatting plugins conflict with stashed
  unstaged changes [#13](https://github.com/greenbone/autohooks/pull/13)
* Allow to access config sections via passing an argument list to **config.get**
  e.g. config.get('tools', 'autohooks', 'plugins', 'foo')
  [#15](https://github.com/greenbone/autohooks/pull/15)


[1.1.0]: https://github.com/greenbone/autohooks/compare/v1.0.0...v1.1.0
