# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
