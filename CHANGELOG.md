# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
